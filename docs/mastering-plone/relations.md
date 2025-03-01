---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Relations

You can model relationships between content items by placing them in a hierarchy (e.g. a folder _speakers_ containing the (folderish) speakers and within each speaker the talks) or by linking them to each other in Richtext fields. But where would you then store a talk that two speakers give together?

Relations allow developers to model relationships between objects without using links or a hierarchy. The behavior {py:class}`plone.app.relationfield.behavior.IRelatedItems` provides the field {guilabel}`Related Items` in the tab {guilabel}`Categorization`. That field simply says `a` is somehow related to `b`.

By using custom relations you can model your data in a much more meaningful way.

## Creating and configuring relations in a schema

Relate to one item only.

```{code-block} python
:linenos:

from z3c.relationfield.schema import RelationChoice

evil_mastermind = RelationChoice(
    title="The Evil Mastermind",
    vocabulary="plone.app.vocabularies.Catalog",
    required=False,
)
```

Relate to multiple items.

```{code-block} python
:linenos:

from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList

minions = RelationList(
    title="Minions",
    default=[],
    value_type=RelationChoice(
        title="Minions",
        vocabulary="plone.app.vocabularies.Catalog"
        ),
    required=False,
)
```

We can see that the [code for the behavior IRelatedItems](https://github.com/plone/plone.app.relationfield/blob/master/plone/app/relationfield/behavior.py) does exactly the same.

### Controlling what to relate to

The best way to control wich item should be relatable to is to configure the widget with `directives.widget()`.
In the following example you can only relate to Documents:

```{code-block} python
:emphasize-lines: 12
:linenos:

from plone.app.z3cform.widget import RelatedItemsFieldWidget

relationchoice_field = RelationChoice(
    title="Relationchoice field",
    vocabulary="plone.app.vocabularies.Catalog",
    required=False,
)
directives.widget(
    "relationchoice_field",
    RelatedItemsFieldWidget,
    pattern_options={
        "selectableTypes": ["Document", "Event"],
    },
)
```

### Configure the RelatedItemsFieldWidget

```{note}
These settings only have a effect in Plone 6 Classic.
```

With `pattern_options` you can further configure the widget.

In the following example you can specify a) where to start browsing using the _pattern-option_ `basePath` and and b) to leave the dropwdown open using `closeOnSelect`.

```{code-block} python
:emphasize-lines: 11
:linenos:

relationlist_field = RelationList(
    title="Relationlist Field",
    default=[],
    value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    required=False,
    missing_value=[],
)
directives.widget(
    "relationlist_field",
    RelatedItemsFieldWidget,
    pattern_options={
        "basePath": ",
        "closeOnSelect": False,  # Leave dropdown open for multiple selection
    },
)
```

`basePath` can also be a method. In this exmaple we use the helper-method `plone.app.multilingual.browser.interfaces.make_relation_root_path`.

```{code-block} python
:emphasize-lines: 13
:linenos:

from plone.app.multilingual.browser.interfaces import make_relation_root_path

relationlist_field = RelationList(
    title="Relationlist Field",
    default=[],
    value_type=RelationChoice(vocabulary="plone.app.vocabularies.Catalog"),
    required=False,
    missing_value=[],
)
directives.widget(
    "relationlist_field",
    RelatedItemsFieldWidget,
    pattern_options=make_relation_root_path,
)
```

### Using the search mode of the Related Items Widget

```{note}
These settings only have a effect in Plone 6 Classic.
```

So far we only used the vocabulary `plone.app.vocabularies.Catalog` that returns the full content tree.

Alternatively you can use `CatalogSource` to specify a catalog query that only return the values from the query.

You can pass to `CatalogSource` the same arguments you use for catalog queries.
This makes it very flexible for limiting relateable items by type, path, date, and so on.

Setting the mode of the widget to `search` makes it easier to select from the content that result form your catalog-query instead of having to navigate through your content-tree.

The problem is that in the default mode of the Related Items wisget items that are in container s are not shown unless you add thes types of contaibers to the query.

Therefore is is recommended to use CatalogSource only in in `search` mode.

```{code-block} python
:emphasize-lines: 10
:linenos:

from plone.app.vocabularies.catalog import CatalogSource

speakers = RelationList(
    title="Speaker(s) for this talk",
    value_type=RelationChoice(source=CatalogSource(portal_type="speaker")),
    required=False,
)
directives.widget(
    "speakers",
    RelatedItemsFieldWidget,
    pattern_options={
        "baseCriteria": [  # This is a optimization that limits the catalog-query
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.any",
                "v": ["speaker"],
            }
        ],
        "mode": "search",
    },
)
```

```{figure} _static/relationlist_searchmode.png
:alt: Seach mode of RelationWidget

Search mode of RelationWidget
```

### Define Favorite Locations

The `RelatedItemsFieldWidget` allows you to set favorites:

```{code-block} python
:linenos:

directives.widget(
    "minions",
    RelatedItemsFieldWidget,
    pattern_options={
        "favorites": [{"title": "Minions", "path": "/Plone/minions"}]
    },
)
```

`favorites` can also be a method that takes the current context. Here is a full example as a behavior:

```{code-block} python
:linenos:

from plone import api
from plone.app.vocabularies.catalog import CatalogSource
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


def minion_favorites(context):
    portal = api.portal.get()
    minions_path = "/".join(portal["minions"].getPhysicalPath())
    one_eyed_minions_path = "/".join(portal["one-eyed-minions"].getPhysicalPath())
    return [
            {
                "title": "Current Content",
                "path": "/".join(context.getPhysicalPath())
            }, {
                "title": "Minions",
                "path": minions_path,
            }, {
                "title": "One eyed minions",
                "path": one_eyed_minions_path,
            }
        ]


@provider(IFormFieldProvider)
class IHaveMinions(model.Schema):

    minions = RelationList(
        title="My minions",
        default=[],
        value_type=RelationChoice(
            source=CatalogSource(
                portal_type=["one_eyed_minion", "minion"],
                review_state="published",
            )
        ),
        required=False,
    )
    directives.widget(
        "minions",
        RelatedItemsFieldWidget,
        pattern_options={
            "mode": "auto",
            "favorites": minion_favorites,
            }
        )
```

## RelationFields through the web or in xml

It is surprisingly easy to create RelationFields through the web

- Using the Dexterity schema editor, add a new field and select _Relation List_ or _Relation Choice_, depending on whether you want to relate to multiple items or not.
- When configuring the field you can even select the content type the relation should be limited to.

When you click on `Edit XML field model` you will see the fields in the XML schema:

RelationChoice:

```{code-block} python
:linenos:

<field name="boss" type="z3c.relationfield.schema.RelationChoice">
  <description/>
  <required>False</required>
  <title>Boss</title>
</field>
```

RelationList:

```{code-block} python
:linenos:

<field name="underlings" type="z3c.relationfield.schema.RelationList">
  <description/>
  <required>False</required>
  <title>Underlings</title>
  <value_type type="z3c.relationfield.schema.RelationChoice">
    <title i18n:translate="">Relation Choice</title>
    <portal_type>
      <element>Document</element>
      <element>News Item</element>
    </portal_type>
  </value_type>
</field>
```

## Using different widgets for relations

```{todo}
Support for `StaticCatalogVocabulary` in Volto is currently still missing.
```

Often the standard widget for relations is not what you want since it can be hard to navigate to the content you want to relate to.

If you want to use checkboxes, radiobuttons or a selection-dropdown you need to use `StaticCatalogVocabulary` instead of `CatalogSource` to specify your options.

```{code-block} python
:emphasize-lines: 8, 18
:linenos:

from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from z3c.relationfield.schema import RelationChoice

relationchoice_field_select = RelationChoice(
    title="RelationChoice with Select Widget",
    vocabulary=StaticCatalogVocabulary(
        {
            "portal_type": ["Document", "Event"],
            "review_state": "published",
        }
    ),
    required=False,
)
directives.widget(
    "relationchoice_field_select",
    SelectFieldWidget,
)
```

The field should then look like this:

```{figure} _static/relation_select.png
:alt: RelationList field with select widget

RelationList field with select widget
```

Another example is the `AjaxSelectFieldWidget` that only queries the catalog for results if you start typing:

```{code-block} python
:linenos:

relationlist_field_ajax_select = RelationList(
    title="Relationlist Field with AJAXSelect",
    description="z3c.relationfield.schema.RelationList",
    value_type=RelationChoice(
        vocabulary=StaticCatalogVocabulary(
            {
                "portal_type": ["Document", "Event"],
                "review_state": "published",
            }
        )
    ),
    required=False,
)
directives.widget(
    "relationlist_field_ajax_select",
    AjaxSelectFieldWidget,
    vocabulary=StaticCatalogVocabulary(
        {
            "portal_type": ["Document", "Event", "Folder"],
        },
        title_template="{brain.Type}: {brain.Title} at {path}",
    ),  # Custom item rendering
    pattern_options={  # Options for Select2
        "minimumInputLength": 2,  # - Don't query until at least two characters have been typed
        "ajax": {"quietMillis": 500},  # - Wait 500ms after typing to make query
    },
)
```

```{figure} _static/relationliste_ajax.png
:alt: Relationlist Field with AJAXSelect
```

Relationlist Field with AJAXSelect


## Accessing and displaying related items

To display related items you can use the render method of the default widget e.g.:

```html
<div tal:content="structure view/w/evil_mastermind/render" />
```

This would render the related items like this:

```{figure} https://user-images.githubusercontent.com/453208/77223704-4b714100-6b5f-11ea-855b-c6e209f1c25c.png
:alt: Default rendering of a RelationList (since Plone 5.2.2)
```

If you want to access and render relations yourself you can use the Plone add-on [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers) and add a method like in the following example.

```{code-block} python
:linenos:

from collective.relationhelpers import api as relapi
from Products.Five import BrowserView


class EvilMastermindView(BrowserView):

    def minions(self):
        """Returns a list of related items."""
        return relapi.relations(self.context, "underlings")
```

This returns the related items so that you will able to render them anyhow you like.

## Inspecting relations

You Plone 6 Classic you can inspect all relations and backrelations in your site using the control panel `/@@inspect-relations`.

```{figure} _static/inspect-relations.png
:alt: The relations controlpanel

The relations controlpanel
```

In Plone 5 this is available through the addon [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers).


## Programming with relations

### Plone 6

Since Plone 6 `plone.api` has methods to create, read, and delete relations and backrelations.

```{code-block} python
:linenos:

from plone import api

portal = api.portal.get()
source = portal["bob"]
target = portal["bobby"]
api.relation.create(source=source, target=target, relationship="friend")
```

```{code-block} python
:linenos:

from plone import api

api.relation.get(source=portal["bob"])
api.relation.get(relationship="friend")
api.relation.get(target=portal["bobby"])
```

```{code-block} python
:linenos:

from plone import api

api.relation.delete(source=portal["bob"])
```

See the chapter {ref}`plone6docs:chapter-relation` of the docs for `plone.api`  for more details.


### Plone 5.2 and older

In older Plone-Versions you can use [collective.relationhelpers](https://pypi.org/project/collective.relationhelpers) to create and read relations and backrelations in a very similar way.


### Restapi

A restapi endpoint to create, read, and delete relations and backrelations will be part of `plone.restapi`. See https://github.com/plone/plone.restapi/issues/1432


## Relationfields without relations

A light-weight alternative to using relations is to store a UUID of the object you want to link to. Obviously you will loose the option to query the relation-catalog for these but you could create a custom index for that purpose.

The trick is to use `Choice` and `List` instead of `RelationChoice` or `RelationList` and configure the field to use `RelatedItemsFieldWidget`:

```{code-block} python
:linenos:

from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives
from zope import schema

uuid_choice_field = schema.Choice(
    title="Choice field with RelatedItems widget storing uuids",
    description="schema.Choice",
    vocabulary="plone.app.vocabularies.Catalog",
    required=False,
)
directives.widget("uuid_choice_field", RelatedItemsFieldWidget)
```

Again you can use `StaticCatalogVocabulary` if you want to use alternative widgets. The following example uses Checkboxes:

```{code-block} python
:linenos:

from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from plone.autoform import directives
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema

uuid_list_field_checkbox = schema.List(
    title="RelationList with Checkboxes storing uuids",
    vocabulary=StaticCatalogVocabulary(
        {
            "portal_type": "Document",
            "review_state": "published",
        }
    ),
    required=False,
)
directives.widget(
    "uuid_list_field_checkbox",
    CheckBoxFieldWidget,
)
```

```{note}
For control panels this is the best way to store relations since you cannot store `RelationValue` objects in the registry.
```

## The stack

Relations are based on [zc.relation](https://pypi.org/project/zc.relation/).
This package stores transitive and intransitive relationships.
It allows complex relationships and searches along them.
Because of this functionality, the package is a bit complicated.

The package `zc.relation` provides its own catalog, a relation catalog.
This is a storage optimized for the queries needed.
`zc.relation` is sort of an outlier with regards to Zope documentation. It has extensive documentation, with a good level of doctests for explaining things.

You can use `zc.relation` to store the objects and its relations directly into the catalog.
But the additional packages that make up the relation functionality don't use the catalog this way.

We want to work with schemas to get auto generated forms.
The logic for this is provided by the package [z3c.relationfield](https://pypi.org/project/z3c.relationfield/).
This package contains the RelationValue object and everything needed to define a relation schema, and all the code that is necessary to automatically update the catalog.

A RelationValue Object does not reference all objects directly.
For the target, it uses an id it gets from the `IntId` Utility. This id allows direct recovery of the object. The source object stores it directly.

Widgets are provided by `plone.app.z3cform` and some converters are provided by `plone.app.relationfield`.
The widget that Plone uses can also store objects directly.
Because of this, the following happens when saving a relation via a form:

1. The HTML shows some nice representation of selectable objects.
2. When the user submits the form, selected items are submitted by their UUIDs.
3. The Widget retrieves the original object with the UUID.
4. Some datamanager gets another unique ID from an IntID Tool.
5. The same datamanager creates a RelationValue from this id, and stores this relation value on the source object.
6. Some Event handlers update the catalogs.

You could delete a Relation like this `delattr(rel.from_object, rel.from_attribute)`

This is a terrible idea by the way, because when you define in your schema that one can store multiple RelationValues, your Relation is stored in a list on this attribute.

Relations depend on a lot of infrastructure to work.
This infrastructure in turn depends a lot on event handlers being thrown properly.
When this is not the case things can break.
Because of this, there is a method `isBroken` which you can use to check if the target is available.

There are alternatives to using Relations. You could instead just store the UUID of an object.
But using real relations and the catalog allows for very powerful things.
The simplest concrete advantage is the possibility to see what links to your object.

The built-in linkintegrity feature of Plone 5 is also implemented using relations.

### RelationValues

RelationValue objects have a fairly complete API.
For both target and source, you can receive the IntId, the object and the path.
On a RelationValue, the terms `source` and `target` aren't used. Instead, they are `from` and `to`.
So the API for getting the target is:

- `to_id`
- `to_path`
- `to_object`

In addition, the relation value knows under which attribute it has been stored as `from_attribute`. It is usually the name of the field with which the relation is created.
But it can also be the name of a relation that is created by code, e.g. linkintegrity relations (`isReferencing`) or the relation between a working copy and the original (`iterate-working-copy`).
