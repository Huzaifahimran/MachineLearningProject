import tkinter as tk
import requests

def send_prediction():
    #Get values from entry fields
    credit_score = int(credit_score_entry.get())
    age = int(age_entry.get())
    tenure = int(tenure_entry.get())
    balance = int(balance_entry.get())
    products_number = int(products_number_entry.get())
    credit_card_1 = int(credit_card_1_entry.get())
    active_member_1 = int(active_member_1_entry.get())
    estimated_salary = int(estimated_salary_entry.get())

    country = country_var.get()  
    gender = gender_var.get()    

    #Prepare data payload
    data = {
        "credit_score": credit_score,
        "country_France": 1 if country == "France" else 0,
        "country_Spain": 1 if country == "Spain" else 0,
        "country_Germany": 1 if country == "Germany" else 0,
        "gender_Female": 1 if gender == "Female" else 0,
        "gender_Male": 1 if gender == "Male" else 0,
        "age": age,
        "tenure": tenure,
        "balance": balance,
        "products_number": products_number,
        "credit_card_1": credit_card_1,
        "active_member_1": active_member_1,
        "estimated_salary": estimated_salary,
    }

    #send post request to the api
    response = requests.post("http://127.0.0.1:5000/predict", json=data)

    
    prediction_label.config(text=f"Prediction: {response.text}")


window = tk.Tk()
window.title("Bank Customer Churn Prediction")


features = [
    ("Credit Score:", "credit_score"),
    ("Age:", "age"),
    ("Tenure:", "tenure"),
    ("Balance:", "balance"),
    ("Products Number:", "products_number"),
    ("Credit Card:", "credit_card_1"),
    ("Active Member:", "active_member_1"),
    ("Estimated Salary:", "estimated_salary"),
]


row_counter = 0

for label_text, entry_name in features:
    label = tk.Label(window, text=label_text)
    label.grid(row=row_counter, column=0, padx=5, pady=5, sticky="w")
    
    entry = tk.Entry(window)
    entry.grid(row=row_counter, column=1, padx=5, pady=5)
    
    globals()[f"{entry_name}_entry"] = entry
    
    row_counter += 1

country_var = tk.StringVar(window)
country_var.set("France")  
country_label = tk.Label(window, text="Country:")
country_label.grid(row=8, column=0)
country_optionmenu = tk.OptionMenu(window, country_var, "France", "Spain", "Germany")
country_optionmenu.grid(row=8, column=1)


gender_var = tk.StringVar(window)
gender_var.set("Female")  
gender_label = tk.Label(window, text="Gender:")
gender_label.grid(row=9, column=0)
gender_optionmenu = tk.OptionMenu(window, gender_var, "Female", "Male")
gender_optionmenu.grid(row=9, column=1)


submit_button = tk.Button(window, text="Submit", command=send_prediction)
submit_button.grid(row=10, column=0, columnspan=2, pady=10)


prediction_label = tk.Label(window, text="")
prediction_label.grid(row=11, column=0, columnspan=2)


window.mainloop()
