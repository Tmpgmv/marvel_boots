from concurrency.exceptions import RecordModifiedError, VersionChangedError, VersionError


class ConcurrentUpdateMixin:
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except (RecordModifiedError, VersionChangedError, VersionError):

            form.add_error(None,
                           "⚠️ Товар изменён другим пользователем! "
                           "Вернитесь в список и откройте заново."
                           )
            return self.form_invalid(form)
