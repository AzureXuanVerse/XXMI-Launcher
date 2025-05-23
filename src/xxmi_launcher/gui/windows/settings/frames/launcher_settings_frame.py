import re
import webbrowser

from pathlib import Path
from textwrap import dedent
from customtkinter import ThemeManager
from urllib.parse import urlparse

import core.event_manager as Events
import core.config_manager as Config
import core.path_manager as Paths
import core.i18n_manager as I18n
import gui.vars as Vars

from gui.classes.containers import UIFrame, UIScrollableFrame
from gui.classes.widgets import UILabel, UIButton, UIEntry, UICheckbox,  UIOptionMenu


class LauncherSettingsFrame(UIScrollableFrame):
    def __init__(self, master):
        super().__init__(master, height=360, corner_radius=0, border_width=0)

        # Auto close
        self.put(StartBehaviorLabel(self)).grid(row=0, column=0, padx=(20, 10), pady=(0, 30), sticky='w')
        self.put(StartBehaviorFrame(self)).grid(row=0, column=1, padx=10, pady=(0, 30), sticky='w', columnspan=3)

        # Update Policy
        self.put(UpdatePolicyLabel(self)).grid(row=1, column=0, padx=(20, 10), pady=(0, 30), sticky='w')
        self.put(UpdatePolicyFrame(self)).grid(row=1, column=1, padx=10, pady=(0, 30), sticky='w', columnspan=3)

        # Theme
        self.put(ThemeLabel(self)).grid(row=2, column=0, padx=(20, 10), pady=(0, 30), sticky='w')
        self.put(ThemeFrame(self)).grid(row=2, column=1, padx=10, pady=(0, 30), sticky='w', columnspan=3)

        # Connection
        self.put(ConnectionLabel(self)).grid(row=3, column=0, padx=(20, 10), pady=(0, 30), sticky='w')
        self.put(ConnectionFrame(self)).grid(row=3, column=1, padx=10, pady=(0, 30), sticky='ew', columnspan=3)

        # Proxy
        self.put(ProxyEnableCheckbox(self)).grid(row=4, column=0, padx=(20, 10), pady=(0, 20), sticky='w')
        self.put(ProxySettingsFrame(self)).grid(row=4, column=1, padx=10, pady=(0, 20), sticky='w', columnspan=3)
        self.put(ProxyAddressFrame(self)).grid(row=5, column=1, padx=10, pady=(0, 20), sticky='w', columnspan=3)
        self.put(ProxyCredentialsFrame(self)).grid(row=6, column=1, padx=10, pady=(0, 20), sticky='w', columnspan=3)


class StartBehaviorFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(AutoCloseCheckbox(self)).grid(row=0, column=0, padx=(0, 10), pady=0, sticky='w')
        self.put(TimeoutLabel(self)).grid(row=0, column=1, padx=(20, 10), pady=0, sticky='w')
        self.put(TimeoutEntry(self)).grid(row=0, column=2, padx=(0, 20), pady=0, sticky='w')

        self.grab(TimeoutLabel).set_tooltip(self.grab(TimeoutEntry))


class UpdatePolicyFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(AutoUpdateCheckbox(self)).grid(row=0, column=0, padx=(0, 10), pady=0, sticky='w')
        self.put(UpdateChannelLabel(self)).grid(row=0, column=1, padx=(20, 10), pady=0, sticky='w')
        self.put(UpdateChannelOptionMenu(self)).grid(row=0, column=2, padx=(0, 20), pady=0, sticky='w')

        self.grab(UpdateChannelLabel).set_tooltip(self.grab(UpdateChannelOptionMenu))


class ThemeFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(LauncherThemeOptionMenu(self)).grid(row=0, column=0, padx=(0, 10), pady=0, sticky='w')
        self.put(ApplyThemeButton(self)).grid(row=0, column=1, padx=(10, 10), pady=0, sticky='w')
        self.put(EnableDevMode(self)).grid(row=0, column=2, padx=(20, 20), pady=0, sticky='w')


class ConnectionFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(GitHubTokenLabel(self)).grid(row=0, column=0, padx=(0, 10), pady=0, sticky='w')
        self.put(GitHubTokenFrame(self)).grid(row=0, column=1, padx=(0, 10), pady=0, sticky='ew')
        self.put(VerifySSLCheckbox(self)).grid(row=0, column=2, padx=(20, 20), pady=0, sticky='w')

        self.grab(GitHubTokenLabel).set_tooltip(self.grab(GitHubTokenFrame).grab(GitHubTokenEntry))


class GitHubTokenFrame(UIFrame):
    def __init__(self, master):
        super().__init__(
            border_color = ThemeManager.theme["CTkEntry"].get("border_color", None),
            border_width = ThemeManager.theme["CTkEntry"].get("border_width", None),
            fg_color = ThemeManager.theme["CTkEntry"].get("fg_color", None),
            master=master)

        self.grid_columnconfigure(0, weight=100)

        self.put(GitHubTokenEntry(self)).grid(row=0, column=0, padx=(4, 0), pady=(2, 0), sticky='new')
        self.put(GitHubTokenButton(self)).grid(row=0, column=1, padx=(0, 4), pady=(2, 2), sticky='ne')


class ProxySettingsFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(ProxyTypeLabel(self)).grid(row=0, column=0, padx=(0, 10), pady=0, sticky='w')
        self.put(ProxyTypeOptionMenu(self)).grid(row=0, column=1, padx=(0, 10), pady=0, sticky='w')
        self.put(ProxyDNSViaSocks5Checkbox(self)).grid(row=0, column=2, padx=20, pady=0, sticky='w')

        self.grab(ProxyTypeLabel).set_tooltip(self.grab(ProxyTypeOptionMenu))


class ProxyAddressFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')

        self.put(ProxyHostLabel(self)).grid(row=0, column=0, padx=(0, 0), pady=0, sticky='w')
        self.put(ProxyHostEntry(self)).grid(row=0, column=1, padx=10, pady=0, sticky='w')
        self.put(ProxyPortLabel(self)).grid(row=0, column=2, padx=(10, 0), pady=0, sticky='w')
        self.put(ProxyPortEntry(self)).grid(row=0, column=3, padx=10, pady=0, sticky='w')
        self.put(ProxyUseCredentialsCheckbox(self)).grid(row=0, column=4, padx=20, pady=0, sticky='w')

        self.grab(ProxyHostLabel).set_tooltip(self.grab(ProxyHostEntry))
        self.grab(ProxyPortLabel).set_tooltip(self.grab(ProxyPortEntry))

        self.trace_write(Vars.Launcher.proxy.enable, self.handle_write_proxy_enable)

    def handle_write_proxy_enable(self, var, val):
        for element in self.elements.values():
            if val:
                element.configure(state='normal')
            else:
                element.configure(state='disabled')


class ProxyCredentialsFrame(UIFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color='transparent')
        self.hide()

        self.put(ProxyUserLabel(self)).grid(row=0, column=0, padx=(0, 0), pady=(0, 30), sticky='w')
        self.put(ProxyUserEntry(self)).grid(row=0, column=1, padx=10, pady=(0, 30), sticky='w')
        self.grab(ProxyUserLabel).set_tooltip(self.grab(ProxyUserEntry))

        self.put(ProxyPasswordLabel(self)).grid(row=0, column=2, padx=(10, 0), pady=(0, 30), sticky='w')
        self.put(ProxyPasswordEntry(self)).grid(row=0, column=3, padx=10, pady=(0, 30), sticky='w')
        self.grab(ProxyPasswordLabel).set_tooltip(self.grab(ProxyPasswordEntry))

        self.trace_write(Vars.Launcher.proxy.enable, self.handle_write_proxy_enable)
        self.trace_write(Vars.Launcher.proxy.use_credentials, self.handle_write_use_credentials)

    def handle_write_proxy_enable(self, var, val):
        for element in self.elements.values():
            if val and Vars.Launcher.proxy.use_credentials.get():
                element.configure(state='normal')
            else:
                element.configure(state='disabled')

    def handle_write_use_credentials(self, var, val):
        for element in self.elements.values():
            if val and Vars.Launcher.proxy.enable.get():
                element.configure(state='normal')
            else:
                element.configure(state='disabled')


class StartBehaviorLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.start_behavior'),
            font=('Microsoft YaHei', 14, 'bold'),
            fg_color='transparent',
            master=master)


class AutoCloseCheckbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.close_after_start'),
            variable=Vars.Launcher.auto_close,
            master=master)
        self.set_tooltip(I18n._('tooltip.auto_close'))


class TimeoutLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.timeout'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class TimeoutEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.start_timeout,
            width=40,
            height=36,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.timeout'))

        self.configure(validate='key', validatecommand=(master.register(self.validate_input), '%P'))

    @staticmethod
    def validate_input(value):
        return value.isdigit()


class UpdatePolicyLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.update_policy'),
            font=('Microsoft YaHei', 14, 'bold'),
            fg_color='transparent',
            master=master)


class AutoUpdateCheckbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.auto_update'),
            variable=Vars.Launcher.auto_update,
            master=master)
        self.set_tooltip(self.get_tooltip)

    def get_tooltip(self):
        return I18n._('tooltip.auto_update').format(importer=Config.Launcher.active_importer)


class UpdateChannelLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.channel'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class UpdateChannelOptionMenu(UIOptionMenu):
    def __init__(self, master):
        super().__init__(
            values=['Auto', 'MSI', 'ZIP'],
            variable=Vars.Launcher.update_channel,
            width=100,
            height=36,
            font=('Arial', 14),
            dropdown_font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.update_channel'))


class ThemeLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.ui_theme'),
            font=('Microsoft YaHei', 14, 'bold'),
            fg_color='transparent',
            master=master)


class LauncherThemeOptionMenu(UIOptionMenu):
    def __init__(self, master):
        super().__init__(
            values=['Default'],
            variable=Vars.Launcher.gui_theme,
            width=150,
            height=36,
            font=('Arial', 14),
            dropdown_font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.launcher_theme'))

    def update_values(self):
        values = ['Default']
        for path in Paths.App.Themes.iterdir():
            if path.is_dir() and path.name != 'Default':
                values.append(path.name)
        self.configure(values=values)

    def _open_dropdown_menu(self):
        self.update_values()
        super()._open_dropdown_menu()


class ApplyThemeButton(UIButton):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.apply'),
            command=self.apply_theme,
            width=100,
            height=36,
            font=('Roboto', 14),
            master=master)

        self.trace_write(Vars.Launcher.gui_theme, self.handle_write_gui_theme)

        self.hide()

    def apply_theme(self):
        Events.Fire(Events.Application.CloseSettings(save=True))
        Events.Fire(Events.Application.Restart(delay=0))

    def handle_write_gui_theme(self, var, val):
        if val != Config.Config.active_theme:
            self.show()
        else:
            self.hide()


class EnableDevMode(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.dev_mode'),
            variable=Vars.Launcher.theme_dev_mode,
            master=master)
        self.set_tooltip(I18n._('tooltip.dev_mode'))

        self.trace_write(Vars.Launcher.theme_dev_mode, self.handle_write_theme_dev_mode)

    def handle_write_theme_dev_mode(self, var, val):
        Config.Config.Launcher.theme_dev_mode = val
        Events.Fire(Events.GUI.ToggleThemeDevMode(enabled=val))


class ConnectionLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.connection'),
            font=('Microsoft YaHei', 14, 'bold'),
            fg_color='transparent',
            master=master)


class GitHubTokenLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.github_token'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class GitHubTokenEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.github_token,
            width=280,
            height=32,
            border_width=0,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.github_token'))


class GitHubTokenButton(UIButton):
    def __init__(self, master):
        fg_color = ThemeManager.theme['CTkEntry'].get('fg_color', None)
        super().__init__(
            text=I18n._('settings.launcher.create'),
            command=lambda: webbrowser.open('https://github.com/settings/tokens'),
            auto_width=True,
            padx=6,
            height=32,
            border_width=0,
            font=('Roboto', 14),
            fg_color=fg_color,
            hover_color=fg_color,
            text_color=['#000000', '#aaaaaa'],
            text_color_hovered=['#000000', '#ffffff'],
            master=master)

        self.set_tooltip(I18n._('tooltip.github_token_button'))


class VerifySSLCheckbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.verify_ssl'),
            variable=Vars.Launcher.verify_ssl,
            master=master)
        self.set_tooltip(I18n._('tooltip.verify_ssl'))


class ProxyEnableCheckbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.use_proxy'),
            font=('Microsoft YaHei', 14, 'bold'),
            variable=Vars.Launcher.proxy.enable,
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_enable'))


class ProxyTypeLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.proxy_type'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)

        self.trace_write(Vars.Launcher.proxy.enable, self.handle_write_proxy_enable)

    def handle_write_proxy_enable(self, var, val):
        if val:
            self.configure(state='normal')
        else:
            self.configure(state='disabled')


class ProxyTypeOptionMenu(UIOptionMenu):
    def __init__(self, master):
        super().__init__(
            values=['HTTPS', 'SOCKS5'],
            variable=Vars.Launcher.proxy.type,
            width=140,
            height=36,
            font=('Arial', 14),
            dropdown_font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_type'))

        self.trace_write(Vars.Launcher.proxy.enable, self.handle_write_proxy_enable)

    def handle_write_proxy_enable(self, var, val):
        if val:
            self.configure(state='normal')
        else:
            self.configure(state='disabled')


class ProxyDNSViaSocks5Checkbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.proxy_dns'),
            variable=Vars.Launcher.proxy.proxy_dns_via_socks5,
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_dns'))

        self.trace_write(Vars.Launcher.proxy.enable, self.handle_write_proxy_enable)
        self.trace_write(Vars.Launcher.proxy.type, self.handle_write_proxy_type)

    def handle_write_proxy_enable(self, var, val):
        if val and Vars.Launcher.proxy.type.get() == 'SOCKS5':
            self.configure(state='normal')
        else:
            self.configure(state='disabled')

    def handle_write_proxy_type(self, var, val):
        if val == 'SOCKS5' and Vars.Launcher.proxy.enable.get():
            self.configure(state='normal')
        else:
            self.configure(state='disabled')


class ProxyHostLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.host'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class ProxyHostEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.proxy.host,
            width=130,
            height=36,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_host'))

        self.trace_write(Vars.Launcher.proxy.host, self.handle_write_host)

    def handle_write_host(self, var, value):
        value = value.strip()

        if not value:
            var.set('')
            return

        scheme = ''
        if 'http' not in value:
            if len(re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})').findall(value)) == 1:
                scheme = 'tcp://'
            else:
                scheme = 'https://'

        result = urlparse(scheme+value)

        if result.hostname is not None:
            var.set(result.hostname)

        if result.port is not None:
            Vars.Launcher.proxy.port.set(result.port)


class ProxyPortLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.port'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class ProxyPortEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.proxy.port,
            width=55,
            height=36,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_port'))

        self.trace_write(Vars.Launcher.proxy.port, self.handle_write_port)

    def handle_write_port(self, var, value):
        value = value.strip()
        if not value:
            var.set('')
            return
        for part in reversed(value.split(':')):
            if not part:
                continue
            result = re.compile(r'(\d+)').findall(part)
            if len(result) > 0:
                var.set(result[-1])
                return
        var.set('')


class ProxyUseCredentialsCheckbox(UICheckbox):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.proxy_auth'),
            variable=Vars.Launcher.proxy.use_credentials,
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_auth'))


class ProxyUserLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.user'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class ProxyUserEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.proxy.user,
            width=130,
            height=36,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_user'))


class ProxyPasswordLabel(UILabel):
    def __init__(self, master):
        super().__init__(
            text=I18n._('settings.launcher.password'),
            font=('Microsoft YaHei', 14),
            fg_color='transparent',
            master=master)


class ProxyPasswordEntry(UIEntry):
    def __init__(self, master):
        super().__init__(
            textvariable=Vars.Launcher.proxy.password,
            width=250,
            height=36,
            font=('Arial', 14),
            master=master)
        self.set_tooltip(I18n._('tooltip.proxy_password'))
