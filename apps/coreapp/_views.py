from apps.coreapp.models.profile import Profile


class ProfileDataMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.dbfunctions.get_user_active_profile(self.request.user.id)
        context['profiles'] = Profile.dbfunctions.get_user_profiles(self.request.user.id)
        return context
