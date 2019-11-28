from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, Index, fields
from .models import Note

INDEX = Index('search_notes')

INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

my_analyzer = analyzer(
    'my_analyzer',
    tokenizer=tokenizer('standard'),
    filter=['lowercase', 'stop', 'trim'],
    char_filter=["html_strip"]
)


@registry.register_document
@INDEX.document
class NoteDocument(Document):
    """Note Elastic search document."""

    class Django:
        model = Note

    id = fields.StringField(attr='id', analyzer="standard")

    title = fields.StringField(
        fields={
            'raw': fields.KeywordField(),
        }
    )

    user = fields.StringField(
        attr='user_indexing',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    content = fields.StringField(
        fields={
            'raw': fields.KeywordField(),
        }
    )

    label = fields.StringField(
        attr='label_indexing',
        fields={
            'raw': fields.KeywordField()
        }
    )

    collaborator = fields.StringField(
        attr='collaborator_indexing',
        fields={
            'raw': fields.KeywordField(),
        }
    )
    is_archive = fields.BooleanField()
    is_pin = fields.BooleanField()
    is_trash = fields.BooleanField()
    reminder = fields.DateField()
