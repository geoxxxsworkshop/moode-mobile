import os
from kivy.app import App
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

CONFIG_FILE = "moode_config.json"

class MoodeMobileApp(App):
    def build(self):
        # Haetaan Android-laitteen turvallinen tallennuskansio asetuksille
        data_dir = self.user_data_dir
        self.store = JsonStore(os.path.join(data_dir, CONFIG_FILE))

        # Pääasettelu
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Otsikko
        self.label = Label(
            text="moOde Audio Mobile",
            font_size='24sp',
            size_hint_y=None,
            height=50,
            color=(0.11, 0.73, 0.33, 1)  # moOde-vihreä
        )
        self.main_layout.addWidget(self.label)

        # Ohjeteksti
        self.sub_label = Label(
            text="Syötä moOde-laitteen IP tai osoite:",
            font_size='16sp',
            size_hint_y=None,
            height=30
        )
        self.main_layout.addWidget(self.sub_label)

        # Haetaan aiemmin tallennettu osoite, oletuksena 'moode.local'
        saved_address = "moode.local"
        if self.store.exists('settings'):
            saved_address = self.store.get('settings')['address']

        self.address_input = TextInput(
            text=saved_address,
            multiline=False,
            font_size='18sp',
            size_hint_y=None,
            height=50,
            halign='center'
        )
        self.main_layout.addWidget(self.address_input)

        # Painike
        self.connect_btn = Button(
            text="Yhdistä soittimeen",
            font_size='18sp',
            size_hint_y=None,
            height=60,
            background_color=(0.11, 0.73, 0.33, 1),
            background_normal=''
        )
        self.connect_btn.bind(on_press=self.open_moode)
        self.main_layout.addWidget(self.connect_btn)

        return self.main_layout

    def open_moode(self, instance):
        address = self.address_input.text.strip()
        if not address:
            return

        # Puhdistetaan osoite urliin sopivaksi
        if address.startswith("http://"):
            address = address[7:]
        elif address.startswith("https://"):
            address = address[8:]

        # Tallennetaan osoite puhelimen muistiin
        self.store.put('settings', address=address)
        target_url = f"http://{address}"

        # Tyhjennetään aloitusnäkymä puhelimen ruudulta
        self.main_layout.clear_widgets()
        
        try:
            from android.runnable import run_on_ui_thread
            from jnius import autoclass

            # Kutsutaan Androidin laitteistotason komponentteja
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            activity = autoclass('org.kivy.android.PythonActivity').mActivity

            @run_on_ui_thread
            def create_webview():
                webview = WebView(activity)
                
                # ERITTÄIN TÄRKEÄT ASETUKSET MOODELLE:
                webview.getSettings().setJavaScriptEnabled(True)
                webview.getSettings().setDomStorageEnabled(True)  # Sallii paikallisen välimuistin
                webview.getSettings().setBuiltInZoomControls(True) # Sallii zoomauksen tarvittaessa
                webview.getSettings().setDisplayZoomControls(False)
                
                webview.setWebViewClient(WebViewClient())
                webview.loadUrl(target_url)
                activity.setContentView(webview)

            create_webview()
        except Exception as e:
            # Varmistus virhetilanteita varten
            error_label = Label(text=f"WebView-virhe: {e}", font_size='14sp')
            self.main_layout.addWidget(error_label)


if __name__ == '__main__':
    MoodeMobileApp().run()
