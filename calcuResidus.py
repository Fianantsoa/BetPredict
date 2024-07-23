import csv
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import r2_score
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout








class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        title = Label(text='Predicte', font_size=32, size_hint=(1, 0.2))
        layout.add_widget(title)

        buttons_layout = BoxLayout(orientation='horizontal', spacing=10)

        add_button = Button(text='Ajouter', size_hint=(1, 0.5), background_color=(0.5, 0.5, 1, 1))
        add_button.bind(on_press=self.go_to_add)
        buttons_layout.add_widget(add_button)

        predict_button = Button(text='Predire', size_hint=(1, 0.5), background_color=(0.5, 1, 0.5, 1))
        predict_button.bind(on_press=self.go_to_predict)
        buttons_layout.add_widget(predict_button)

        supprimer_button = Button(text='Supprimer', size_hint=(1, 0.5), background_color=(1, 0 , 0, 1))  # Red color for the button
        supprimer_button.bind(on_press=self.clear_data)  # New function to clear data
        buttons_layout.add_widget(supprimer_button)

        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def go_to_add(self, instance):
        self.manager.current = 'add'

    def go_to_predict(self, instance):
        self.manager.current = 'predict'

    def clear_data(self, instance):
        # Function to clear data from "numero.csv"
        with open('numero.csv', 'r') as f:
            lines = f.readlines()

        with open('numero.csv', 'w') as f:
            f.write(lines[0])  # Write only the first line

        # Show a message after clearing data (optional)
        # message = "Data cleared successfully!"
        # self.show_message(message) 

class AddNumbersScreen(Screen):
    def __init__(self, **kwargs):
        super(AddNumbersScreen, self).__init__(**kwargs)
        self.selected_numbers = []

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        back_button = Button(text='Retour', size_hint=(0.2, 0.1), background_color=(0.5, 0.5, 1, 1))
        back_button.bind(on_press=self.go_back)
        
        validate_button = Button(text='Valider', size_hint=(0.2, 0.1), background_color=(0.5, 0.5, 1, 1))
        validate_button.bind(on_press=self.validate_numbers)

        self.buttons_layout = GridLayout(cols=10, spacing=10, size_hint=(1, 0.8))
        self.buttons = {}
        for i in range(1, 81):
            btn = Button(text=str(i), background_color=(1, 1, 1, 1), font_size='20sp')
            btn.bind(on_press=self.toggle_button)
            self.buttons[i] = btn
            self.buttons_layout.add_widget(btn)
        layout.add_widget(self.buttons_layout)

        buttons_layout_b = GridLayout(cols=10, spacing=10, size_hint=(1, 0.1))
        buttons_layout_b.add_widget(back_button)
        buttons_layout_b.add_widget(validate_button)
        layout.add_widget(buttons_layout_b)

        self.add_widget(layout)

    def toggle_button(self, instance):
        number = int(instance.text)
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
            instance.background_color = (1, 1, 1, 1)  # released
        elif len(self.selected_numbers) < 20:
            self.selected_numbers.append(number)
            instance.background_color = (0.5, 0.5, 1, 1)  # dark blue

    def validate_numbers(self, instance):
        if len(self.selected_numbers) == 20:
            self.save_numbers()
            self.show_info('Ajout terminé', 'Les 20 numéros ont été ajoutés à numero.csv')
            self.reset_buttons()
        else:
            self.show_error('Erreur', 'Vous devez sélectionner exactement 20 numéros.')

    def save_numbers(self):
        file_path = 'numero.csv'
        try:
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.selected_numbers)
        except Exception as e:
            self.show_error('Erreur', f"Une erreur s'est produite : {str(e)}")

    def reset_buttons(self):
        self.selected_numbers.clear()
        for btn in self.buttons.values():
            btn.background_color = (1, 1, 1, 1)

    def show_info(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def show_error(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


class PredictionScreen(Screen):
    def __init__(self, **kwargs):
        super(PredictionScreen, self).__init__(**kwargs)
        self.predictions = []

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        buttons_layout_b = GridLayout(cols=10, spacing=10, size_hint=(1, 0.1))

        back_button = Button(text='Retour', size_hint=(2, 0.2), background_color=(0.5, 0.5, 1, 1))
        back_button.bind(on_press=self.go_back)
        buttons_layout_b.add_widget(back_button)

        self.grid = GridLayout(cols=10, spacing=5, padding=10, size_hint=(1, 0.6))
        self.draw_numbers()  # Call draw_numbers initially to display all numbers
        layout.add_widget(self.grid)

        predict_button = Button(text='Prédire', size_hint=(2, 0.2), background_color=(0.5, 1, 0.5, 1))
        predict_button.bind(on_press=self.predict)
        buttons_layout_b.add_widget(predict_button)

        add_csv_button = Button(text='Ajouter', size_hint=(2, 0.2), background_color=(0.5, 0.5, 1, 1))
        add_csv_button.bind(on_press=self.add)
        buttons_layout_b.add_widget(add_csv_button)
        layout.add_widget(buttons_layout_b)

        self.add_widget(layout)

    def add(self, instance):
        if len(self.predictions) == 20:
            file_path = 'numero.csv'
            try:
                with open(file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(self.predictions)
                print(f"Added predictions to CSV: {self.predictions}")
            except Exception as e:
                self.show_error('Erreur', f"Une erreur s'est produite : {str(e)}")
        else:
            self.show_error('Erreur', f"On ne peut pas ajouter des nombres vides")

    def predict(self, instance):
        try:
            # Lire les données depuis le fichier CSV
            data = pd.read_csv('numero.csv')
            if data.empty:
                self.show_error('Erreur', 'Le fichier numero.csv est vide.')
                return

            # Normaliser les données
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data)

            # Initialisation d'un dictionnaire pour stocker les modèles
            models = {}
            n_columns = data.shape[1]

            for num in range(n_columns):
                y = data_scaled[:, num]  # Extraire la colonne à prédire
                X = np.delete(data_scaled, num, axis=1)  # Utiliser toutes les autres colonnes comme caractéristiques
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Créer et entraîner le modèle de forêt aléatoire
                model = RandomForestRegressor()
                model.fit(X_train, y_train)

                # Évaluation du modèle avec validation croisée
                scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
                rmse_scores = np.sqrt(-scores)
                print(f"RMSE for num_{num}: {rmse_scores.mean()}")

                # Stocker le modèle dans le dictionnaire
                models[f'num_{num}'] = model

            # Générer des prédictions pour une nouvelle séquence
            # Utiliser la dernière ligne comme entrée pour prédire la prochaine séquence
            last_row = data_scaled[-1, :-1].reshape(1, -1)

            self.predictions = []
            for num in range(n_columns):
                model = models[f'num_{num}']
                predicted_number = model.predict(last_row)[0]
                self.predictions.append(int(scaler.inverse_transform([[predicted_number]])[0][0]))

            print(f"Generated predictions: {self.predictions}")
            self.draw_numbers()

        except Exception as e:
            self.show_error('Erreur', f"Une erreur s'est produite : {str(e)}")

    def draw_numbers(self):
        self.grid.clear_widgets()

        all_numbers = list(range(1, 81))

        for number in all_numbers:
            color = [1, 1, 1, 1]  # Blanc par défaut pour tous les chiffres
            if number in self.predictions:
                color = [0, 1, 0, 1]  # Vert pour les chiffres prédits

            label = Label(text=str(number), color=color, font_size='20sp')
            self.grid.add_widget(label)


    def show_error(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AddNumbersScreen(name='add'))
        sm.add_widget(PredictionScreen(name='predict'))

        return sm

if __name__ == '__main__':
    MainApp().run()
