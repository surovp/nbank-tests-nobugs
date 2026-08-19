from src.main.ui.pages.base_page import BasePage


class Profile(BasePage):

    @property
    def profile_text(self):
        return self.page.get_by_text("✏️ Edit Profile")

    @property
    def save_changes_button(self):
        return self.page.get_by_role("button", name="💾 Save Changes")



    def url(self):
        return "/edit-profile"

    def edit_profile(self, name: str = None):
        self.page.get_by_placeholder('Enter new name').clear()
        self.page.get_by_placeholder('Enter new name').fill(name)
        self.save_changes_button.click()
        return self