import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from tkinter import simpledialog
import os

# Base class for all person-related entities
class Person:
    def __init__(self, id, name, address, contact_details):
        self.id = id
        self.name = name
        self.address = address
        self.contact_details = contact_details

class Employee(Person):
    def __init__(self, id, name, address, contact_details, job_title, salary):
        super().__init__(id, name, address, contact_details)
        self.job_title = job_title
        self.salary = salary

class Client(Person):
    def __init__(self, id, name, address, contact_details, budget):
        super().__init__(id, name, address, contact_details)
        self.budget = budget

class Supplier:
    def __init__(self, id, name, service_type, contact_details):
        self.id = id
        self.name = name
        self.service_type = service_type
        self.contact_details = contact_details

class Event:
    def __init__(self, id, type, date, venue, client_id):
        self.id = id
        self.type = type
        self.date = date
        self.venue = venue
        self.client_id = client_id
        self.guest_list = []
        self.suppliers = []

# Helper function to handle file operations
def save_data(data, filename):
    try:
        with open(os.path.join(data_path, filename), 'wb') as dumpf:
            pickle.dump(data, dumpf)
    except Exception as e:
        print("An error occurred while saving the data:", e)

def load_data(filename):
    try:
        with open(os.path.join(data_path, filename), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        print("Data file not found. Starting with an empty dataset.")
        return {}
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return {}


class EventManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Event Management System')
        self.geometry('800x600')
        self.data_files = {'employees': 'employees.pkl', 'clients': 'clients.pkl', 'suppliers': 'suppliers.pkl', 'events': 'events.pkl'}
        self.data = {key: load_data(file) for key, file in self.data_files.items()}
        self.setup_ui()

    def setup_ui(self):
        tab_control = ttk.Notebook(self)
        self.tabs = {name: ttk.Frame(tab_control) for name in ['Employees', 'Clients', 'Suppliers', 'Events']}
        for name, frame in self.tabs.items():
            tab_control.add(frame, text=name)
        tab_control.pack(expand=1, fill="both")
        self.setup_employees_tab()

    def clear_table(self, tree):
        # Clear table data
        for item in tree.get_children():
            tree.delete(item)

    def setup_employees_tab(self):
        frame = self.tabs['Employees']

        ttk.Button(frame, text="Load Employee for Editing", command=self.load_employee_for_editing).grid(row=6,
                                                                                                         column=4)

        ttk.Label(frame, text="Employee ID:").grid(row=0, column=0)
        self.emp_id = ttk.Entry(frame)
        self.emp_id.grid(row=0, column=1)

        ttk.Label(frame, text="Name:").grid(row=1, column=0)
        self.emp_name = ttk.Entry(frame)
        self.emp_name.grid(row=1, column=1)

        ttk.Label(frame, text="Address:").grid(row=2, column=0)
        self.emp_address = ttk.Entry(frame)
        self.emp_address.grid(row=2, column=1)

        ttk.Label(frame, text="Contact Details:").grid(row=3, column=0)
        self.emp_contact = ttk.Entry(frame)
        self.emp_contact.grid(row=3, column=1)

        ttk.Label(frame, text="Job Title:").grid(row=4, column=0)
        self.emp_job_title = ttk.Entry(frame)
        self.emp_job_title.grid(row=4, column=1)

        ttk.Label(frame, text="Salary:").grid(row=5, column=0)
        self.emp_salary = ttk.Entry(frame)
        self.emp_salary.grid(row=5, column=1)

        ttk.Button(frame, text="Add Employee", command=self.add_employee).grid(row=6, column=0)
        ttk.Button(frame, text="Modify Employee", command=self.modify_employee).grid(row=6, column=2)
        ttk.Button(frame, text="Show Employee", command=self.show_employee).grid(row=6, column=3)

        ttk.Label(frame, text="Enter ID to Delete:").grid(row=8, column=0)
        self.delete_emp_id = ttk.Entry(frame)
        self.delete_emp_id.grid(row=8, column=1)
        ttk.Button(frame, text="Delete Employee", command=self.delete_employee).grid(row=8, column=2)

        ttk.Button(frame, text="Find Employee by ID", command=self.find_by_id).grid(row=9, column=0)

        # Employee Table
        self.emp_tree = ttk.Treeview(frame, columns=('Name', 'Address', 'Contact Details', 'Job Title', 'Salary'),
                                     show='headings')
        self.emp_tree.heading('Name', text='Name')
        self.emp_tree.heading('Address', text='Address')
        self.emp_tree.heading('Contact Details', text='Contact Details')
        self.emp_tree.heading('Job Title', text='Job Title')
        self.emp_tree.heading('Salary', text='Salary')
        self.emp_tree.grid(row=7, column=0, columnspan=4, pady=10)
        self.update_employee_table()

    def add_employee(self):
        # Add employee to data
        emp_id = self.emp_id.get()
        emp_name = self.emp_name.get()
        emp_address = self.emp_address.get()
        emp_contact = self.emp_contact.get()
        emp_job_title = self.emp_job_title.get()
        emp_salary = self.emp_salary.get()

        if emp_id and emp_name and emp_address and emp_contact and emp_job_title and emp_salary:
            if emp_id not in self.data['employees']:
                self.data['employees'][emp_id] = Employee(emp_id, emp_name, emp_address, emp_contact, emp_job_title, emp_salary)
                save_data(self.data['employees'], self.data_files['employees'])
                self.update_employee_table()
                messagebox.showinfo('Success', 'Employee added successfully!')
            else:
                messagebox.showerror('Error', 'Employee ID already exists!')
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def delete_employee(self):
        # Retrieve the ID from the delete-specific entry widget
        emp_id = self.delete_emp_id.get().strip()
        if emp_id:
            if emp_id in self.data['employees']:
                del self.data['employees'][emp_id]
                save_data(self.data['employees'], self.data_files['employees'])
                self.update_employee_table()
                messagebox.showinfo('Success', 'Employee deleted successfully!')
                self.delete_emp_id.delete(0, 'end')  # Clear the entry field after deletion
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to delete.')

    def show_employee(self):
        # Display employee details
        emp_id = self.emp_id.get()
        if emp_id:
            if emp_id in self.data['employees']:
                employee = self.data['employees'][emp_id]
                messagebox.showinfo('Employee Details', f'ID: {employee.id}\nName: {employee.name}\nAddress: {employee.address}\nContact: {employee.contact_details}\nJob Title: {employee.job_title}\nSalary: {employee.salary}')
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to show details.')

    def update_employee_table(self):
        # Update employee table
        self.clear_table(self.emp_tree)
        for emp_id, emp in self.data['employees'].items():
            self.emp_tree.insert('', 'end', text=emp_id, values=(emp.name, emp.address, emp.contact_details, emp.job_title, emp.salary))


    def load_employee_for_editing(self):
        emp_id = self.emp_id.get().strip()  # Get the ID from the entry widget
        if emp_id:
            if emp_id in self.data['employees']:
                employee = self.data['employees'][emp_id]
                # Fill the form fields with the employee data
                self.emp_name.delete(0, tk.END)  # Clear the existing entry first
                self.emp_name.insert(0, employee.name)

                self.emp_address.delete(0, tk.END)
                self.emp_address.insert(0, employee.address)

                self.emp_contact.delete(0, tk.END)
                self.emp_contact.insert(0, employee.contact_details)

                self.emp_job_title.delete(0, tk.END)
                self.emp_job_title.insert(0, employee.job_title)

                self.emp_salary.delete(0, tk.END)
                self.emp_salary.insert(0, employee.salary)
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to load for editing.')

    def modify_employee(self):
        emp_id = simpledialog.askstring("Modify Employee", "Enter the ID of the employee to modify")
        if emp_id in self.data['employees']:
            employee = self.data['employees'][emp_id]

            # Ask for new values for each attribute
            new_name = simpledialog.askstring("Modify Employee", "Enter new name (leave blank if no change):")
            new_address = simpledialog.askstring("Modify Employee", "Enter new address (leave blank if no change):")
            new_contact = simpledialog.askstring("Modify Employee",
                                                 "Enter new contact details (leave blank if no change):")
            new_job_title = simpledialog.askstring("Modify Employee", "Enter new job title (leave blank if no change):")
            new_salary = simpledialog.askstring("Modify Employee", "Enter new salary (leave blank if no change):")

            # Update attributes if new values are provided
            if new_name:
                employee.name = new_name
            if new_address:
                employee.address = new_address
            if new_contact:
                employee.contact_details = new_contact
            if new_job_title:
                employee.job_title = new_job_title
            if new_salary:
                employee.salary = new_salary

            # Save the updated data
            save_data(self.data['employees'], self.data_files['employees'])
            self.update_employee_table()
            messagebox.showinfo('Success', 'Employee updated successfully!')
        else:
            messagebox.showerror('Error', 'Employee ID not found!')

    def find_by_id(self):
        emp_id = simpledialog.askstring("Find Employee", "Enter the Employee ID:")
        if emp_id and emp_id in self.data['employees']:
            employee = self.data['employees'][emp_id]
            employee_details = (
                f"ID: {employee.id}\n"
                f"Name: {employee.name}\n"
                f"Address: {employee.address}\n"
                f"Contact Details: {employee.contact_details}\n"
                f"Job Title: {employee.job_title}\n"
                f"Salary: {employee.salary}"
            )
            messagebox.showinfo("Employee Details", employee_details)
        else:
            messagebox.showerror("Error", "Employee ID not found or invalid ID!")

    def setup_clients_tab(self, frame):
        ttk.Label(frame, text="Client ID:").grid(row=0, column=0)
        self.client_id = ttk.Entry(frame)
        self.client_id.grid(row=0, column=1)

        ttk.Label(frame, text="Name:").grid(row=1, column=0)
        self.client_name = ttk.Entry(frame)
        self.client_name.grid(row=1, column=1)

        ttk.Label(frame, text="Address:").grid(row=2, column=0)
        self.client_address = ttk.Entry(frame)
        self.client_address.grid(row=2, column=1)

        ttk.Label(frame, text="Contact Details:").grid(row=3, column=0)
        self.client_contact = ttk.Entry(frame)
        self.client_contact.grid(row=3, column=1)

        ttk.Label(frame, text="Budget:").grid(row=4, column=0)
        self.client_budget = ttk.Entry(frame)
        self.client_budget.grid(row=4, column=1)

        ttk.Button(frame, text="Add Client", command=self.add_client).grid(row=5, column=1)
        ttk.Button(frame, text="Modify Client", command=self.modify_client).grid(row=5, column=2)
        ttk.Button(frame, text="Delete Client", command=self.delete_client).grid(row=5, column=3)
        ttk.Button(frame, text="Find Client by ID", command=self.find_client_by_id).grid(row=5, column=4)

    def add_client(self):
        client_id = self.client_id.get().strip()
        name = self.client_name.get().strip()
        address = self.client_address.get().strip()
        contact = self.client_contact.get().strip()
        budget = self.client_budget.get().strip()

        # Validate input fields are not empty
        if not all([client_id, name, address, contact, budget]):
            messagebox.showerror('Error', 'All fields must be filled out!')
            return

        try:
            budget = float(budget)  # Ensure budget is a valid number
        except ValueError:
            messagebox.showerror('Error', 'Budget must be a numeric value.')
            return

        if client_id in self.data['clients']:
            messagebox.showerror('Error', 'A client with this ID already exists!')
            return

        # Create new client instance and add to data
        new_client = Client(client_id, name, address, contact, budget)
        self.data['clients'][client_id] = new_client
        save_data(self.data['clients'], self.data_files['clients'])
        messagebox.showinfo('Success', 'Client added successfully!')

    def modify_client(self):
        client_id = self.client_id.get().strip()
        if client_id not in self.data['clients']:
            messagebox.showerror('Error', 'Client ID not found!')
            return

        name = self.client_name.get().strip()
        address = self.client_address.get().strip()
        contact = self.client_contact.get().strip()
        budget = self.client_budget.get().strip()

        try:
            budget = float(budget) if budget else self.data['clients'][client_id].budget
        except ValueError:
            messagebox.showerror('Error', 'Budget must be a numeric value.')
            return

        client = self.data['clients'][client_id]
        client.name = name if name else client.name
        client.address = address if address else client.address
        client.contact_details = contact if contact else client.contact_details
        client.budget = budget if budget else client.budget

        save_data(self.data['clients'], self.data_files['clients'])
        messagebox.showinfo('Success', 'Client details updated successfully!')

    def delete_client(self):
        client_id = self.client_id.get().strip()
        if client_id in self.data['clients']:
            del self.data['clients'][client_id]
            save_data(self.data['clients'], self.data_files['clients'])
            messagebox.showinfo('Success', 'Client deleted successfully!')
        else:
            messagebox.showerror('Error', 'Client ID not found!')

    def find_client_by_id(self):
        client_id = self.client_id.get().strip()
        client = self.data['clients'].get(client_id)
        if client:
            details = f"ID: {client.id}\nName: {client.name}\nAddress: {client.address}\nContact Details: {client.contact_details}\nBudget: {client.budget}"
            messagebox.showinfo('Client Details', details)
        else:
            messagebox.showerror('Error', 'Client ID not found!')

    def setup_suppliers_tab(self, frame):
        ttk.Label(frame, text="Supplier ID:").grid(row=0, column=0)
        self.sup_id = ttk.Entry(frame)
        self.sup_id.grid(row=0, column=1)

        ttk.Label(frame, text="Name:").grid(row=1, column=0)
        self.sup_name = ttk.Entry(frame)
        self.sup_name.grid(row=1, column=1)

        ttk.Label(frame, text="Service Type:").grid(row=2, column=0)
        self.sup_service_type = ttk.Entry(frame)
        self.sup_service_type.grid(row=2, column=1)

        ttk.Label(frame, text="Contact Details:").grid(row=3, column=0)
        self.sup_contact = ttk.Entry(frame)
        self.sup_contact.grid(row=3, column=1)

        ttk.Button(frame, text="Add Supplier", command=self.add_supplier).grid(row=4, column=1)
        ttk.Button(frame, text="Modify Supplier", command=self.modify_supplier).grid(row=4, column=2)
        ttk.Button(frame, text="Delete Supplier", command=self.delete_supplier).grid(row=4, column=3)
        ttk.Button(frame, text="Find Supplier by ID", command=self.find_supplier_by_id).grid(row=4, column=4)

    def add_supplier(self):
        supplier_id = self.sup_id.get().strip()
        name = self.sup_name.get().strip()
        service_type = self.sup_service_type.get().strip()
        contact = self.sup_contact.get().strip()

        if not all([supplier_id, name, service_type, contact]):
            messagebox.showerror('Error', 'All fields must be filled out!')
            return

        if supplier_id in self.data['suppliers']:
            messagebox.showerror('Error', 'A supplier with this ID already exists!')
            return

        new_supplier = Supplier(supplier_id, name, service_type, contact)
        self.data['suppliers'][supplier_id] = new_supplier
        save_data(self.data['suppliers'], self.data_files['suppliers'])
        messagebox.showinfo('Success', 'Supplier added successfully!')

    def modify_supplier(self):
        supplier_id = self.sup_id.get().strip()
        if supplier_id not in self.data['suppliers']:
            messagebox.showerror('Error', 'Supplier ID not found!')
            return

        name = self.sup_name.get().strip()
        service_type = self.sup_service_type.get().strip()
        contact = self.sup_contact.get().strip()

        supplier = self.data['suppliers'][supplier_id]
        supplier.name = name if name else supplier.name
        supplier.service_type = service_type if service_type else supplier.service_type
        supplier.contact_details = contact if contact else supplier.contact_details

        save_data(self.data['suppliers'], self.data_files['suppliers'])
        messagebox.showinfo('Success', 'Supplier details updated successfully!')

    def delete_supplier(self):
        supplier_id = self.sup_id.get().strip()
        if supplier_id in self.data['suppliers']:
            del self.data['suppliers'][supplier_id]
            save_data(self.data['suppliers'], self.data_files['suppliers'])
            messagebox.showinfo('Success', 'Supplier deleted successfully!')
        else:
            messagebox.showerror('Error', 'Supplier ID not found!')

    def find_supplier_by_id(self):
        supplier_id = self.sup_id.get().strip()
        supplier = self.data['suppliers'].get(supplier_id)
        if supplier:
            details = f"ID: {supplier.id}\nName: {supplier.name}\nService Type: {supplier.service_type}\nContact Details: {supplier.contact_details}"
            messagebox.showinfo('Supplier Details', details)
        else:
            messagebox.showerror('Error', 'Supplier ID not found!')

    def setup_events_tab(self, frame):
        ttk.Label(frame, text="Event ID:").grid(row=0, column=0)
        self.event_id = ttk.Entry(frame)
        self.event_id.grid(row=0, column=1)

        ttk.Label(frame, text="Type:").grid(row=1, column=0)
        self.event_type = ttk.Entry(frame)
        self.event_type.grid(row=1, column=1)

        ttk.Label(frame, text="Date:").grid(row=2, column=0)
        self.event_date = ttk.Entry(frame)
        self.event_date.grid(row=2, column=1)

        ttk.Label(frame, text="Venue:").grid(row=3, column=0)
        self.event_venue = ttk.Entry(frame)
        self.event_venue.grid(row=3, column=1)

        ttk.Label(frame, text="Client ID:").grid(row=4, column=0)
        self.event_client_id = ttk.Entry(frame)
        self.event_client_id.grid(row=4, column=1)

        ttk.Button(frame, text="Add Event", command=self.add_event).grid(row=5, column=1)
        ttk.Button(frame, text="Modify Event", command=self.modify_event).grid(row=5, column=2)
        ttk.Button(frame, text="Delete Event", command=self.delete_event).grid(row=5, column=3)
        ttk.Button(frame, text="Find Event by ID", command=self.find_event_by_id).grid(row=5, column=4)

    def add_event(self):
        event_id = self.event_id.get().strip()
        type = self.event_type.get().strip()
        date = self.event_date.get().strip()
        venue = self.event_venue.get().strip()
        client_id = self.event_client_id.get().strip()

        if not all([event_id, type, date, venue, client_id]):
            messagebox.showerror('Error', 'All fields must be filled out!')
            return

        if event_id in self.data['events']:
            messagebox.showerror('Error', 'An event with this ID already exists!')
            return

        if client_id not in self.data['clients']:
            messagebox.showerror('Error', 'Client ID does not exist!')
            return

        new_event = Event(event_id, type, date, venue, client_id)
        self.data['events'][event_id] = new_event
        save_data(self.data['events'], self.data_files['events'])
        messagebox.showinfo('Success', 'Event added successfully!')

    def modify_event(self):
        event_id = self.event_id.get().strip()
        if event_id not in self.data['events']:
            messagebox.showerror('Error', 'Event ID not found!')
            return

        type = self.event_type.get().strip()
        date = self.event_date.get().strip()
        venue = self.event_venue.get().strip()
        client_id = self.event_client_id.get().strip()

        if client_id and client_id not in self.data['clients']:
            messagebox.showerror('Error', 'Client ID does not exist!')
            return

        event = self.data['events'][event_id]
        event.type = type if type else event.type
        event.date = date if date else event.date
        event.venue = venue if venue else event.venue
        event.client_id = client_id if client_id else event.client_id

        save_data(self.data['events'], self.data_files['events'])
        messagebox.showinfo('Success', 'Event details updated successfully!')

    def delete_event(self):
        event_id = self.event_id.get().strip()
        if event_id in self.data['events']:
            del self.data['events'][event_id]
            save_data(self.data['events'], self.data_files['events'])
            messagebox.showinfo('Success', 'Event deleted successfully!')
        else:
            messagebox.showerror('Error', 'Event ID not found!')

    def find_event_by_id(self):
        event_id = self.event_id.get().strip()
        event = self.data['events'].get(event_id)
        if event:
            details = f"ID: {event.id}\nType: {event.type}\nDate: {event.date}\nVenue: {event.venue}\nClient ID: {event.client_id}"
            messagebox.showinfo('Event Details', details)
        else:
            messagebox.showerror('Error', 'Event ID not found!')


if __name__ == "__main__":
    app = EventManagementApp()
    app.mainloop()
