# Convert an existing page to a folder with that page as the default page
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py
#   - Access to object

# Specify page to be converted
context = site.restrictedTraverse('/path/to/page')

# Specify new id for default page
default_page_id = 'default'

# Get containing object
parent = context.aq_parent

# Imports
from Products.CMFCore.utils import getToolByName

# Dump page to .zexp file as a backup
parent.manage_exportObject(id=page_id, download=False)

# Get basic information about the page
page_uid = context.UID()
page_id = context.getId()
page_title = context.getRawTitle()
page_description = context.getRawDescription()
page_subject = context.getRawSubject()
page_creators = context.getRawCreators()
page_contributors = context.getRawContributors()
page_exclude_from_nav = context.getRawExcludeFromNav()
page_effective_date = context.getRawEffectiveDate()
page_owner = context.getOwner()

# Get roles for page
page_roles = context.get_local_roles()

# Get workflow state for page
wftool = getToolByName(site, "portal_workflow")
page_review_state = wftool.getInfoFor(context, 'review_state')

# Get position index of page
page_position = parent.getObjectPosition(page_id)

# Rename page to temporary id (UID concatenated with id)
tmp_id = '%s-%s' % (page_uid, page_id)
parent.manage_renameObject(page_id, tmp_id)

# Create folder with same id and information
parent.invokeFactory(id=page_id, type_name="Folder", title=page_title,
                     description=page_description, subject=page_subject,
                     creators=page_creators, contributors=page_contributors,
                     exclude_from_nav=page_exclude_from_nav,
                     effective=page_effective_date)

# Get newly created folder
o = parent[page_id]

# Change ownership
o.changeOwnership(page_owner)

# Set local roles for folder
for (i,j) in page_roles:
    o.manage_setLocalRoles(i, j)

# Move new folder to previous page position
parent.moveObjectToPosition(page_id, page_position)

# Note that it's been successfully created
o.unmarkCreationFlag()

# If page was published, publish folder. Assumes standard workflow.
if page_review_state == 'published':
    wftool.doActionFor(o, 'publish')

# Reindex folder
o.reindexObject()

# Reindex folder security
o.reindexObjectSecurity()

# Move (cut/paste) the existing page (now with tmp_id) into that folder
cb_copy_data = parent.manage_cutObjects(ids=[tmp_id])
o.manage_pasteObjects(cb_copy_data=cb_copy_data)

# Rename from tmp_id to 'default'
o.manage_renameObjects(ids=[tmp_id], new_ids=[default_page_id])

# Set default page for folder
o.setDefaultPage(default_page_id)

# Remove tags from default page
context.setSubject([])
context.reindexObject()

# commit transaction to ZODB
transaction.commit()