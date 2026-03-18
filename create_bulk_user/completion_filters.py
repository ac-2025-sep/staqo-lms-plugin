# import logging

# from crum import get_current_request, get_current_user
# from openedx_filters.filters import PipelineStep
# from lms.djangoapps.course_api.blocks.api import get_blocks
# from lms.djangoapps.course_api.blocks.views import recurse_mark_complete
# from xmodule.modulestore.django import modulestore

# LOGGER = logging.getLogger(__name__)


# def _safe_is_course_completed(request, user, course_key):
#     try:
#         course_usage_key = modulestore().make_course_usage_key(course_key)

#         blocks_response = get_blocks(
#             request=request,
#             usage_key=course_usage_key,
#             user=user,
#             depth="all",
#             requested_fields=["completion"],
#             block_counts=[],
#             student_view_data=[],
#             return_type="dict",
#             block_types_filter=None,
#             nav_depth=None,
#             hide_access_denials=False,
#         )

#         root = blocks_response.get("root")
#         blocks = blocks_response.get("blocks", {})
#         if not root or root not in blocks:
#             return False

#         recurse_mark_complete(root, blocks)
#         return blocks[root].get("completion") == 1
#     except Exception as exc:
#         LOGGER.exception(
#             "Could not compute completion for user=%s course=%s: %s",
#             getattr(user, "id", None),
#             str(course_key),
#             str(exc),
#         )
#         return False


# class AddCompletionFlagToEnrollment(PipelineStep):
#     def run_filter(self, course_key, serialized_enrollment, **kwargs):
#         user = get_current_user()
#         request = get_current_request()

#         if not user or getattr(user, "is_anonymous", True) or request is None:
#             return {
#                 "course_key": course_key,
#                 "serialized_enrollment": serialized_enrollment,
#             }

#         updated = dict(serialized_enrollment or {})
#         updated["isCompleted"] = _safe_is_course_completed(request, user, course_key)

#         return {
#             "course_key": course_key,
#             "serialized_enrollment": updated,
#         }
