# Globally replace "from_tag" with "to_tag"
#
# Assumptions:
#   - set-site.py
#   - login-as-admin.py
#   - Access to object

# Imports
from Products.CMFCore.utils import getToolByName

# Define tags as from_ and to_ tags.

from_tag = 'my-from-tag'
to_tag = 'my-to-tag'

# Query catalog for items tagged with from_tag
portal_catalog = getToolByName(site, "portal_catalog")
results = portal_catalog.searchResults({'Subject' : from_tag})

# Iterate through brains:
#  * Verify that from_tag is present and remove it
#  * Verify to_tag is not present, and add it
#  * Update subject
#  * Reindex item (for catalog)

for r in results:
    o = r.getObject()
    s = list(o.Subject())
    if from_tag in s:
        s.remove(from_tag)
        if to_tag not in s:
            s.append(to_tag)
        o.setSubject(tuple(s))
        o.reindexObject()

# commit transaction to ZODB
transaction.commit()