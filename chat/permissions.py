from rest_framework import permissions
# from groups.models import get_user_groups
# 
# class IsChannelMember(permissions.BasePermission):
#     """
#     Custom permission to allow only members of a channel or members of a group
#     attached to a channel to interact with it according to their ACL (read,
#     write, admin).
#     It also prevents any edition on default channel and allow any loged user to
#     use it.
#     """
# 
#     def has_permission(self, request, view):
#         return request.user and request.user.is_authenticated()
# 
#     def has_object_permission(self, request, view, channel):
#         if request.method == 'GET':
#             if channel.public is True:
#                 return True
# 
#             if request.user.is_staff is True:
#                 return True
# 
#             if 'read_channel' in get_perms(request.user, channel):
#                 return True
# 
#             for group in get_user_groups(request.user):
#                 if 'read_channel' in get_perms(group, channel):
#                     return True
# 
#             return False
# 
#         if request.method == 'POST':
#             if channel.id == 1:
#                 return False
# 
#             return True
# 
#         if request.method == 'DELETE':
#             if channel.id == 1:
#                 return False
# 
#             for user, permissions in channel_members:
#                 # only admins can update or delete a channel
#                 if request.user == user and permissions == 'a':
#                     return True
# 
#             for group, permissions in channel_groups:
#                 if (request.user in get_group_members(group) and
#                     permissions == 'a'):
#                     return True
# 
#             return False
