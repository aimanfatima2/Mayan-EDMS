from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from navigation.api import register_links, register_top_menu, \
    register_model_list_columns, register_multi_item_links, \
    register_sidebar_template
from main.api import register_diagnostic, register_tool
from permissions.api import register_permission, set_namespace_title
from tags.widgets import get_tags_inline_widget_simple
from history.api import register_history_type

from documents.models import Document, DocumentPage, \
    DocumentPageTransformation, DocumentType, DocumentTypeFilename
from documents.staging import StagingFile
from documents.conf.settings import USE_STAGING_DIRECTORY
from documents.conf.settings import PER_USER_STAGING_DIRECTORY
from documents.literals import PERMISSION_DOCUMENT_CREATE, \
    PERMISSION_DOCUMENT_PROPERTIES_EDIT, PERMISSION_DOCUMENT_VIEW, \
    PERMISSION_DOCUMENT_DELETE, PERMISSION_DOCUMENT_DOWNLOAD, \
    PERMISSION_DOCUMENT_TRANSFORM, PERMISSION_DOCUMENT_TOOLS, \
    PERMISSION_DOCUMENT_EDIT
from documents.literals import PERMISSION_DOCUMENT_TYPE_EDIT, \
    PERMISSION_DOCUMENT_TYPE_DELETE, PERMISSION_DOCUMENT_TYPE_CREATE
from documents.literals import HISTORY_DOCUMENT_CREATED, \
    HISTORY_DOCUMENT_EDITED, HISTORY_DOCUMENT_DELETED

# Permission setup
set_namespace_title('documents', _(u'Documents'))
register_permission(PERMISSION_DOCUMENT_CREATE)
register_permission(PERMISSION_DOCUMENT_PROPERTIES_EDIT)
register_permission(PERMISSION_DOCUMENT_EDIT)
register_permission(PERMISSION_DOCUMENT_VIEW)
register_permission(PERMISSION_DOCUMENT_DELETE)
register_permission(PERMISSION_DOCUMENT_DOWNLOAD)
register_permission(PERMISSION_DOCUMENT_TRANSFORM)
register_permission(PERMISSION_DOCUMENT_TOOLS)

# Document type permissions
register_permission(PERMISSION_DOCUMENT_TYPE_EDIT)
register_permission(PERMISSION_DOCUMENT_TYPE_DELETE)
register_permission(PERMISSION_DOCUMENT_TYPE_CREATE)

# History setup
register_history_type(HISTORY_DOCUMENT_CREATED)
register_history_type(HISTORY_DOCUMENT_EDITED)
register_history_type(HISTORY_DOCUMENT_DELETED)

document_list = {'text': _(u'all documents'), 'view': 'document_list', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_list_recent = {'text': _(u'recent documents'), 'view': 'document_list_recent', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_create_multiple = {'text': _(u'upload new documents'), 'view': 'document_create_multiple', 'famfam': 'page_add', 'permissions': [PERMISSION_DOCUMENT_CREATE]}
document_create_siblings = {'text': _(u'upload new documents using same metadata'), 'view': 'document_create_siblings', 'args': 'object.id', 'famfam': 'page_copy', 'permissions': [PERMISSION_DOCUMENT_CREATE]}
document_view_simple = {'text': _(u'details (simple)'), 'view': 'document_view_simple', 'args': 'object.id', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_view_advanced = {'text': _(u'details (advanced)'), 'view': 'document_view_advanced', 'args': 'object.id', 'famfam': 'page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_delete = {'text': _(u'delete'), 'view': 'document_delete', 'args': 'object.id', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_multiple_delete = {'text': _(u'delete'), 'view': 'document_multiple_delete', 'famfam': 'page_delete', 'permissions': [PERMISSION_DOCUMENT_DELETE]}
document_edit = {'text': _(u'edit'), 'view': 'document_edit', 'args': 'object.id', 'famfam': 'page_edit', 'permissions': [PERMISSION_DOCUMENT_PROPERTIES_EDIT]}
document_preview = {'text': _(u'preview'), 'class': 'fancybox', 'view': 'document_preview', 'args': 'object.id', 'famfam': 'magnifier', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_download = {'text': _(u'download'), 'view': 'document_download', 'args': 'object.id', 'famfam': 'page_save', 'permissions': [PERMISSION_DOCUMENT_DOWNLOAD]}
document_find_duplicates = {'text': _(u'find duplicates'), 'view': 'document_find_duplicates', 'args': 'object.id', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_find_all_duplicates = {'text': _(u'find all duplicates'), 'view': 'document_find_all_duplicates', 'famfam': 'page_refresh', 'permissions': [PERMISSION_DOCUMENT_VIEW], 'description': _(u'Search all the documents\' checksums and return a list of the exact matches.')}
document_clear_transformations = {'text': _(u'clear all transformations'), 'view': 'document_clear_transformations', 'args': 'object.id', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_multiple_clear_transformations = {'text': _(u'clear all transformations'), 'view': 'document_multiple_clear_transformations', 'famfam': 'page_paintbrush', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_print = {'text': _(u'print'), 'view': 'document_print', 'args': 'object.id', 'famfam': 'printer', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_history_view = {'text': _(u'history'), 'view': 'history_for_object', 'args': ['"documents"', '"document"', 'object.id'], 'famfam': 'book_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'object.id', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_create = {'text': _(u'create new transformation'), 'class': 'no-parent-history', 'view': 'document_page_transformation_create', 'args': 'object.id', 'famfam': 'pencil_add', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_edit = {'text': _(u'edit'), 'class': 'no-parent-history', 'view': 'document_page_transformation_edit', 'args': 'object.id', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_delete = {'text': _(u'delete'), 'class': 'no-parent-history', 'view': 'document_page_transformation_delete', 'args': 'object.id', 'famfam': 'pencil_delete', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}
document_page_transformation_page_view = {'text': _(u'page details'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'object.document_page.id', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_transformation_page_edit = {'text': _(u'edit page'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'object.document_page.id', 'famfam': 'page_white', 'permissions': [PERMISSION_DOCUMENT_EDIT]}
document_page_transformation_page_transformation_list = {'text': _(u'page transformations'), 'class': 'no-parent-history', 'view': 'document_page_transformation_list', 'args': 'object.document_page.id', 'famfam': 'pencil_go', 'permissions': [PERMISSION_DOCUMENT_TRANSFORM]}

document_page_view = {'text': _(u'page image'), 'class': 'no-parent-history', 'view': 'document_page_view', 'args': 'object.id', 'famfam': 'page_white_picture', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_text = {'text': _(u'page text'), 'class': 'no-parent-history', 'view': 'document_page_text', 'args': 'object.id', 'famfam': 'page_white_text', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_edit = {'text': _(u'edit page text'), 'class': 'no-parent-history', 'view': 'document_page_edit', 'args': 'object.id', 'famfam': 'page_white_edit', 'permissions': [PERMISSION_DOCUMENT_EDIT]}
document_page_navigation_next = {'text': _(u'next page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_next', 'args': 'object.id', 'famfam': 'resultset_next', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_navigation_previous = {'text': _(u'previous page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_previous', 'args': 'object.id', 'famfam': 'resultset_previous', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_navigation_first = {'text': _(u'first page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_first', 'args': 'object.id', 'famfam': 'resultset_first', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_navigation_last = {'text': _(u'last page'), 'class': 'no-parent-history', 'view': 'document_page_navigation_last', 'args': 'object.id', 'famfam': 'resultset_last', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_zoom_in = {'text': _(u'zoom in'), 'class': 'no-parent-history', 'view': 'document_page_zoom_in', 'args': 'object.id', 'famfam': 'zoom_in', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_zoom_out = {'text': _(u'zoom out'), 'class': 'no-parent-history', 'view': 'document_page_zoom_out', 'args': 'object.id', 'famfam': 'zoom_out', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_rotate_right = {'text': _(u'rotate right'), 'class': 'no-parent-history', 'view': 'document_page_rotate_right', 'args': 'object.id', 'famfam': 'arrow_turn_right', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_page_rotate_left = {'text': _(u'rotate left'), 'class': 'no-parent-history', 'view': 'document_page_rotate_left', 'args': 'object.id', 'famfam': 'arrow_turn_left', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

document_missing_list = {'text': _(u'Find missing document files'), 'view': 'document_missing_list', 'famfam': 'folder_page', 'permissions': [PERMISSION_DOCUMENT_VIEW]}

upload_document_from_local = {'text': _(u'local'), 'view': 'upload_document_from_local', 'famfam': 'drive_disk', 'keep_query': True}
upload_document_from_staging = {'text': _(u'staging'), 'view': 'upload_document_from_staging', 'famfam': 'drive_network', 'keep_query': True, 'condition': lambda x: USE_STAGING_DIRECTORY}
upload_document_from_user_staging = {'text': _(u'user staging'), 'view': 'upload_document_from_user_staging', 'famfam': 'drive_user', 'keep_query': True, 'condition': lambda x: PER_USER_STAGING_DIRECTORY}

staging_file_preview = {'text': _(u'preview'), 'class': 'fancybox-noscaling', 'view': 'staging_file_preview', 'args': ['source', 'object.id'], 'famfam': 'drive_magnify'}
staging_file_delete = {'text': _(u'delete'), 'view': 'staging_file_delete', 'args': ['source', 'object.id'], 'famfam': 'drive_delete'}

# Document type related links
document_type_list = {'text': _(u'document type list'), 'view': 'document_type_list', 'famfam': 'layout', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_document_list = {'text': _(u'list of documents of this type'), 'view': 'document_type_document_list', 'args': 'object.id', 'famfam': 'page_go', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_edit = {'text': _(u'edit'), 'view': 'document_type_edit', 'args': 'object.id', 'famfam': 'layout_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_delete = {'text': _(u'delete'), 'view': 'document_type_delete', 'args': 'object.id', 'famfam': 'layout_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_DELETE]}
document_type_create = {'text': _(u'create document type'), 'view': 'document_type_create', 'famfam': 'layout_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_CREATE]}

document_type_filename_list = {'text': _(u'document type filenames'), 'view': 'document_type_filename_list', 'args': 'object.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_VIEW]}
document_type_filename_create = {'text': _(u'add filename to document type'), 'view': 'document_type_filename_create', 'args': 'document_type.id', 'famfam': 'database_add', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_edit = {'text': _(u'edit'), 'view': 'document_type_filename_edit', 'args': 'object.id', 'famfam': 'database_edit', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_delete = {'text': _(u'delete'), 'view': 'document_type_filename_delete', 'args': 'object.id', 'famfam': 'database_delete', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}
document_type_filename_return_to_document_type = {'text': _(u'return to document type filenames'), 'view': 'document_type_filename_list', 'args': 'object.document_type.id', 'famfam': 'database', 'permissions': [PERMISSION_DOCUMENT_TYPE_EDIT]}

document_type_views = ['document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete', 'document_type_create', 'document_type_filename_list', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_delete']

# Register document type links
register_links(DocumentType, [document_type_document_list, document_type_filename_list, document_type_edit, document_type_delete])
register_links(DocumentTypeFilename, [document_type_filename_edit, document_type_filename_delete])

register_links(['document_type_filename_delete', 'document_type_create', 'document_type_filename_create', 'document_type_filename_edit', 'document_type_filename_list', 'document_type_list', 'document_type_document_list', 'document_type_edit', 'document_type_delete'], [document_type_create], menu_name='sidebar')
register_links(['document_type_filename_create', 'document_type_filename_list', 'document_type_filename_edit', 'document_type_filename_delete'], [document_type_filename_create], menu_name='sidebar')
register_links(['document_type_filename_edit', 'document_type_filename_delete'], [document_type_filename_return_to_document_type], menu_name='sidebar')

# Register document links 
register_links(Document, [document_view_simple, document_view_advanced, document_edit, document_print, document_delete, document_download, document_find_duplicates, document_clear_transformations, document_history_view])
register_links(Document, [document_create_siblings], menu_name='sidebar')

register_multi_item_links(['document_type_document_list', 'search', 'results', 'document_group_view', 'document_list', 'document_list_recent'], [document_multiple_clear_transformations, document_multiple_delete])

register_links(['document_list_recent', 'document_list', 'document_create', 'document_create_multiple', 'upload_document', 'upload_document_from_local', 'upload_document_from_staging', 'upload_document_from_user_staging', 'document_find_duplicates'], [document_list_recent, document_list, document_create_multiple], menu_name='secondary_menu')

register_links(DocumentPage, [
    document_page_transformation_list, document_page_view,
    document_page_text, document_page_edit,
])

register_links(DocumentPage, [
    document_page_navigation_first, document_page_navigation_previous,
    document_page_navigation_next, document_page_navigation_last
], menu_name='sidebar')

register_links(['document_page_view'], [document_page_rotate_left, document_page_rotate_right, document_page_zoom_in, document_page_zoom_out], menu_name='form_header')

# Upload sources
register_links(['upload_document_from_local', 'upload_document_from_staging', 'upload_document_from_user_staging'], [upload_document_from_local, upload_document_from_staging, upload_document_from_user_staging], menu_name='form_header')

register_links(DocumentPageTransformation, [document_page_transformation_edit, document_page_transformation_delete])
register_links(DocumentPageTransformation, [document_page_transformation_page_edit, document_page_transformation_page_view], menu_name='sidebar')
register_links('document_page_transformation_list', [document_page_transformation_create], menu_name='sidebar')
register_links('document_page_transformation_create', [document_page_transformation_create], menu_name='sidebar')
register_links(['document_page_transformation_edit', 'document_page_transformation_delete'], [document_page_transformation_page_transformation_list], menu_name='sidebar')

register_links(StagingFile, [staging_file_preview, staging_file_delete])

register_diagnostic('documents', _(u'Documents'), document_missing_list)

register_tool(document_find_all_duplicates, namespace='documents', title=_(u'documents'))


def document_exists(document):
    try:
        if document.exists():
            return u'<span class="famfam active famfam-tick"></span>'
        else:
            return u'<span class="famfam active famfam-cross"></span>'
    except Exception, exc:
        return exc

register_model_list_columns(Document, [
        {'name':_(u'thumbnail'), 'attribute':
            lambda x: u'<a class="fancybox" href="%(url)s"><img class="lazy-load" data-href="%(thumbnail)s" src="%(media_url)s/images/ajax-loader.gif" alt="%(string)s" /><noscript><img src="%(thumbnail)s" alt="%(string)s" /></noscript></a>' % {
                'url': reverse('document_preview', args=[x.pk]),
                'thumbnail': reverse('document_thumbnail', args=[x.pk]),
                'media_url': settings.MEDIA_URL,
                'string': _(u'thumbnail')
            }
        },
        {'name':_(u'tags'), 'attribute':
            lambda x: get_tags_inline_widget_simple(x)
        },
        {'name':_(u'metadata'), 'attribute':
            lambda x: x.get_metadata_string()
        },
    ])

register_top_menu('documents', link={'famfam': 'page', 'text': _(u'documents'), 'view': 'document_list_recent'}, children_path_regex=[r'^documents/[^t]', r'^metadata/[^s]', r'comments'], position=0)

register_sidebar_template(['document_list_recent'], 'recent_document_list_help.html')
register_sidebar_template(['document_type_list'], 'document_types_help.html')
