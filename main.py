import flet as ft
import pickle
import os
from datetime import datetime
import csv


DATA_FILE = "expenses_data.pkl"
APP_NAME = ">> REMO_OX << إدارة النفقات"
translations = {
    "ar": {
        "app_title": ">> REMO_OX << إدارة النفقات",
        "income": "إيراد",
        "expense": "مصروف",
        "date": "التاريخ",
        "amount": "المبلغ",
        "category": "التصنيف",
        "description_main": "البيان الرئيسي",
        "description_sub": "البيان الفرعي",
        "notes": "ملاحظات",
        "add_transaction": "إضافة عملية",
        "save": "حفظ",
        "export_csv": "تصدير CSV",
        "language_setting": "اللغة",
        "choose_type": "اختر النوع",
        "income_saved": "تم حفظ الإيراد بنجاح!",
        "expense_saved": "تم حفظ المصروف بنجاح!",
        "amount_required": "المبلغ مطلوب!",
        "category_required": "التصنيف مطلوب!",
        "view_transactions": "عرض المعاملات",
        "all_transactions": "جميع المعاملات",
        "edit": "تعديل",
        "delete": "حذف",
        "confirm_delete_title": "تأكيد الحذف",
        "confirm_delete_message": "هل أنت متأكد أنك تريد حذف هذا الإدخال؟",
        "yes": "نعم",
        "no": "لا",
        "transaction_deleted": "تم حذف المعاملة بنجاح!",
        "transaction_updated": "تم تحديث المعاملة بنجاح!",
        "edit_transaction_title": "تعديل معاملة",
        "cancel": "إلغاء",
        "update": "تحديث",
        "csv_exported_success": "تم تصدير البيانات إلى ملف CSV بنجاح!",
        "csv_export_error": "حدث خطأ أثناء تصدير ملف CSV.",
        "no_data_to_export": "لا توجد بيانات لتصديرها.",
        "type": "النوع",
        # New translations for reporting feature
        "start_date": "تاريخ البدء",
        "end_date": "تاريخ الانتهاء",
        "generate_report": "إنشاء تقرير",
        "report_section": "قسم التقارير",
        "report_summary": "ملخص التقرير",
        "date_range": "النطاق الزمني",
        "total_income": "إجمالي الإيرادات",
        "total_expense": "إجمالي المصروفات",
        "net_balance": "صافي الرصيد",
        "transactions_report_title": "تقرير المعاملات",
        "close": "إغلاق",
        "date_range_required": "يجب تحديد نطاق التاريخ!",
        "invalid_date_format": "صيغة التاريخ غير صالحة!",
    },
    "en": {
        "app_title": "By >> REMO_OX << Expense Manager",
        "income": "Income",
        "expense": "Expense",
        "date": "Date",
        "amount": "Amount",
        "category": "Category",
        "description_main": "Main Description",
        "description_sub": "Sub Description",
        "notes": "Notes",
        "add_transaction": "Add Transaction",
        "save": "Save",
        "export_csv": "Export CSV",
        "language_setting": "Language",
        "choose_type": "Choose Type",
        "income_saved": "Income saved successfully!",
        "expense_saved": "Expense saved successfully!",
        "amount_required": "Amount is required!",
        "category_required": "Category is required!",
        "view_transactions": "View Transactions",
        "all_transactions": "All Transactions",
        "edit": "Edit",
        "delete": "Delete",
        "confirm_delete_title": "Confirm Deletion",
        "confirm_delete_message": "Are you sure you want to delete this entry?",
        "yes": "Yes",
        "no": "No",
        "transaction_deleted": "Transaction deleted successfully!",
        "transaction_updated": "Transaction updated successfully!",
        "edit_transaction_title": "Edit Transaction",
        "cancel": "Cancel",
        "update": "Update",
        "csv_exported_success": "Data exported to CSV successfully!",
        "csv_export_error": "An error occurred while exporting CSV.",
        "no_data_to_export": "No data to export.",
        "type": "Type",
        "start_date": "Start Date",
        "end_date": "End Date",
        "generate_report": "Generate Report",
        "report_section": "Reports Section",
        "report_summary": "Report Summary",
        "date_range": "Date Range",
        "total_income": "Total Income",
        "total_expense": "Total Expense",
        "net_balance": "Net Balance",
        "transactions_report_title": "Transactions Report",
        "close": "Close",
        "date_range_required": "Date range is required!",
        "invalid_date_format": "Invalid date format!",
    },
}


def load_data():
    """Load data from pickle file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return {"transactions": []}

def save_data(data):
    """Save data to pickle file."""
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)


def translate(page, key):
    """Translate a key based on the current language."""
    return translations[page.current_language].get(key, key)

 
def update_input_fields_visibility(page, transaction_type, description_sub_field):
    """Update visibility of input fields based on transaction type."""
    if transaction_type.value == "income":
        description_sub_field.visible = False
    else:
        description_sub_field.visible = True
    
    description_sub_field.update()

def show_message(page, message, color=ft.Colors.GREEN_500):
    """Show a message to the user."""
    page.snack_bar.content = ft.Text(message)
    page.snack_bar.bgcolor = color
    page.snack_bar.open = True
    page.update()

def add_transaction(e, page, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type):
    """Add a transaction to the data."""
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not amount_field.value:
        show_message(page, translate(page, "amount_required"), ft.Colors.RED_500)
        return
    if not category_field.value:
        show_message(page, translate(page, "category_required"), ft.Colors.RED_500)
        return

    try:
        amount = float(amount_field.value)
    except ValueError:
        show_message(page, "المبلغ يجب أن يكون رقمًا صالحًا!" if page.current_language == "ar" else "Amount must be a valid number!", ft.Colors.RED_500)
        return

    new_transaction = {
        "type": transaction_type.value,
        "date": current_date,
        "amount": amount,
        "category": category_field.value,
        "description_main": description_main_field.value,
        "description_sub": description_sub_field.value if transaction_type.value == "expense" else "",
        "notes": notes_field.value,
    }
    page.session_data["transactions"].append(new_transaction)
    show_message(page, translate(page, "income_saved" if transaction_type.value == "income" else "expense_saved"))
    save_data(page.session_data)
    amount_field.value = ""
    category_field.value = ""
    description_main_field.value = ""
    description_sub_field.value = ""
    notes_field.value = ""
    page.update()


def open_date_picker(e, page, target_field):
    """Opens a date picker and updates the target_field with the selected date."""
    def on_date_selected(e):
        target_field.value = e.control.value.strftime("%Y-%m-%d") if e.control.value else ""
        page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_selected,
        on_dismiss=lambda e: print("Date picker dismissed"),
        first_date=datetime(2023, 1, 1), 
        last_date=datetime(2030, 12, 31), 
    )
    
    page.overlay.append(date_picker)
    date_picker.open = True 
    page.update()
    

def generate_transactions_report(page, start_date_field, end_date_field):
    """Generates a report for transactions within a specified date range."""
    start_date_str = start_date_field.value
    end_date_str = end_date_field.value

    if not start_date_str or not end_date_str:
        show_message(page, translate(page, "date_range_required"), ft.Colors.RED_500)
        return

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    except ValueError:
        show_message(page, translate(page, "invalid_date_format"), ft.Colors.RED_500)
        return

    total_income = 0.0
    total_expense = 0.0

    filtered_transactions = []
    for transaction in page.session_data["transactions"]:
        transaction_date = datetime.strptime(transaction["date"].split(" ")[0], "%Y-%m-%d")
        if start_date <= transaction_date <= end_date:
            filtered_transactions.append(transaction)
            if transaction["type"] == "income":
                total_income += transaction["amount"]
            elif transaction["type"] == "expense":
                total_expense += transaction["amount"]
    
    net_balance = total_income - total_expense

    report_content = ft.Column(
        [
            ft.Text(f"{translate(page, 'report_summary')}", size=18, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"{translate(page, 'date_range')}: {start_date_str} - {end_date_str}", size=14),
            ft.Divider(),
            ft.Text(f"{translate(page, 'total_income')}: {total_income:.2f}", size=16, color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD),
            ft.Text(f"{translate(page, 'total_expense')}: {total_expense:.2f}", size=16, color=ft.Colors.RED_700, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"{translate(page, 'net_balance')}: {net_balance:.2f}", size=18, color=ft.Colors.BLUE_700, weight=ft.FontWeight.BOLD),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10
    )

    
    if hasattr(page, 'dialog') and page.dialog in page.overlay:
        page.overlay.remove(page.dialog)
        page.update()

    
    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(translate(page, "transactions_report_title")),
        content=report_content,
        actions=[
            ft.TextButton(translate(page, "close"), on_click=lambda e: (setattr(page.dialog, 'open', False), page.update(), page.overlay.remove(page.dialog) if page.dialog in page.overlay else None)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(page.dialog)
    page.dialog.open = True
    page.update()

def change_language(page, lang, app_bar, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type, save_button, view_transactions_button, choose_type_text_control, start_date_field, end_date_field, generate_report_button, report_section_text):
    """Change the app language and update UI."""
    page.current_language = lang
    app_bar.title.value = translate(page, "app_title")  
    amount_field.label = translate(page, "amount")
    category_field.label = translate(page, "category")
    description_main_field.label = translate(page, "description_main")
    description_sub_field.label = translate(page, "description_sub")
    notes_field.label = translate(page, "notes")
    transaction_type.content.controls[0].label = translate(page, "income")
    transaction_type.content.controls[1].label = translate(page, "expense")
    save_button.text = translate(page, "save")
    view_transactions_button.text = translate(page, "view_transactions")
    app_bar.actions[1].tooltip = translate(page, "export_csv")  
    choose_type_text_control.value = translate(page, "choose_type") 
    start_date_field.label = translate(page, "start_date")
    end_date_field.label = translate(page, "end_date")
    generate_report_button.text = translate(page, "generate_report")
    report_section_text.value = translate(page, "report_section")

    update_input_fields_visibility(page, transaction_type, description_sub_field)
    page.snack_bar.open = False
    page.update()
def delete_transaction(page, index):
    """Delete a transaction from the list."""
    def confirm_delete(e):
        page.dialog.open = False
        if page.dialog in page.overlay:
            page.overlay.remove(page.dialog)
        page.update()
        
        if e.control.text == translate(page, "yes"):
            del page.session_data["transactions"][index]
            save_data(page.session_data)
            show_message(page, translate(page, "transaction_deleted"))
            view_transactions_dialog(page, None)  
        page.update()
    
    if hasattr(page, 'dialog') and page.dialog in page.overlay:
        page.overlay.remove(page.dialog)
        page.update() 

    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(translate(page, "confirm_delete_title")),
        content=ft.Text(translate(page, "confirm_delete_message")),
        actions=[
            ft.TextButton(translate(page, "yes"), on_click=confirm_delete),
            ft.TextButton(translate(page, "no"), on_click=confirm_delete),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(page.dialog)
    page.dialog.open = True
    page.update()

def edit_transaction(page, index, transaction_data):
    """Open a dialog to edit a transaction."""
    edit_amount_field = ft.TextField(
        label=translate(page, "amount"),
        keyboard_type=ft.KeyboardType.NUMBER,
        value=str(transaction_data["amount"]),
        width=300,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string=""),
    )
    edit_category_field = ft.TextField(
        label=translate(page, "category"),
        value=transaction_data["category"],
        width=300,
    )
    edit_description_main_field = ft.TextField(
        label=translate(page, "description_main"),
        multiline=True,
        min_lines=1,
        max_lines=2,
        value=transaction_data["description_main"],
        width=300,
    )
    edit_description_sub_field = ft.TextField(
        label=translate(page, "description_sub"),
        value=transaction_data["description_sub"],
        width=300,
        visible=transaction_data["type"] == "expense",
    )
    edit_notes_field = ft.TextField(
        label=translate(page, "notes"),
        multiline=True,
        min_lines=1,
        max_lines=3,
        value=transaction_data["notes"],
        width=300,
    )

    def update_transaction(e):
        """Save changes to the transaction."""
        try:
            updated_amount = float(edit_amount_field.value)
        except ValueError:
            show_message(page, "المبلغ يجب أن يكون رقمًا صالحًا!" if page.current_language == "ar" else "Amount must be a valid number!", ft.Colors.RED_500)
            return

        if not edit_category_field.value:
            show_message(page, translate(page, "category_required"), ft.Colors.RED_500)
            return

        page.session_data["transactions"][index]["amount"] = updated_amount
        page.session_data["transactions"][index]["category"] = edit_category_field.value
        page.session_data["transactions"][index]["description_main"] = edit_description_main_field.value
        page.session_data["transactions"][index]["description_sub"] = edit_description_sub_field.value if transaction_data["type"] == "expense" else ""
        page.session_data["transactions"][index]["notes"] = edit_notes_field.value
        save_data(page.session_data)
        show_message(page, translate(page, "transaction_updated"))
        
        
        page.dialog.open = False
        if page.dialog in page.overlay:
            page.overlay.remove(page.dialog)
        page.update()
        
        view_transactions_dialog(page, None)  
    
    if hasattr(page, 'dialog') and page.dialog in page.overlay:
        page.overlay.remove(page.dialog)
        page.update()

    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(translate(page, "edit_transaction_title")),
        content=ft.Column([
            edit_amount_field,
            edit_category_field,
            edit_description_main_field,
            edit_description_sub_field,
            edit_notes_field,
        ]),
        actions=[
            ft.TextButton(translate(page, "cancel"), on_click=lambda e: (setattr(page.dialog, 'open', False), page.update(), page.overlay.remove(page.dialog) if page.dialog in page.overlay else None)),
            ft.ElevatedButton(translate(page, "update"), on_click=update_transaction),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.overlay.append(page.dialog)
    page.dialog.open = True
    page.update()

def view_transactions_dialog(page, e):
    all_transactions_list = ft.ListView(
        expand=True,  
        spacing=10,
    )

    if not page.session_data["transactions"]:
        all_transactions_list.controls.append(ft.Text(translate(page, "no_data_to_export"), size=14, text_align=ft.TextAlign.CENTER))
    else:
        for i, transaction in enumerate(page.session_data["transactions"]):
            all_transactions_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        border=ft.border.all(1, ft.Colors.GREY_400),
                        content=ft.Column(
                            [
                                ft.Text(f"{translate(page, 'type')}: {translate(page, transaction['type'])}", size=10, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{translate(page, 'date')}: {transaction['date']}", size=15),
                                ft.Text(f"{translate(page, 'amount')}: {transaction['amount']}", size=15, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{translate(page, 'category')}: {transaction['category']}", size=15),
                                ft.Text(f"{translate(page, 'description_main')}: {transaction['description_main']}", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, size=15),
                                ft.Text(f"{translate(page, 'description_sub')}: {transaction['description_sub']}", max_lines=2, overflow=ft.TextOverflow.ELLIPSIS, visible=transaction["type"] == "expense", size=15),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            tooltip=translate(page, "edit"),
                                            icon_size=19,
                                            on_click=lambda ev, idx=i, tx=transaction: edit_transaction(page, idx, tx)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            tooltip=translate(page, "delete"),
                                            icon_size=19,
                                            on_click=lambda ev, idx=i: delete_transaction(page, idx)
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END
                                )
                            ],
                            spacing=5,
                        )
                    ),
                    elevation=2,
                )
            )


    dialog_content_container = ft.Container(
        content=all_transactions_list,
        height=300,  
        width=350, 
    )

    
    if hasattr(page, 'dialog') and page.dialog in page.overlay:
        page.overlay.remove(page.dialog)
        page.update() 

    
    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(translate(page, "all_transactions")),
        content=dialog_content_container,
        actions=[
            ft.TextButton(translate(page, "cancel"), on_click=lambda e: (setattr(page.dialog, 'open', False), page.update(), page.overlay.remove(page.dialog) if page.dialog in page.overlay else None)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    
    page.overlay.append(page.dialog)
    page.dialog.open = True
    page.update()

def export_to_csv(page):
    """Export transactions to a CSV file."""
    if not page.session_data["transactions"]:
        show_message(page, translate(page, "no_data_to_export"), ft.Colors.ORANGE_500)
        return

    fieldnames = ["type", "date", "amount", "category", "description_main", "description_sub", "notes"]
    try:
        import os
        download_path = "/storage/emulated/0/Download/expenses_report.csv"
        with open(download_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            translated_fieldnames = [translate(page, f) for f in fieldnames]
            writer = csv.DictWriter(csvfile, fieldnames=translated_fieldnames)
            writer.writeheader()
            for transaction in page.session_data["transactions"]:
                row_data = {translate(page, k): v for k, v in transaction.items() if k in fieldnames}
                if transaction["type"] == "income" and "description_sub" in row_data:
                    row_data[translate(page, "description_sub")] = ""
                writer.writerow(row_data)
        show_message(page, translate(page, "csv_exported_success"), ft.Colors.BLUE_500)
    except Exception as e:
        show_message(page, f"{translate(page, 'csv_export_error')}: {e}", ft.Colors.RED_500)


def main(page: ft.Page):
    page.title = APP_NAME
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 700
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.GREY_300
    page.session_data = load_data()
    page.current_language = "ar" 

    
    app_bar = ft.AppBar(
        title=ft.Text(translate(page, "app_title"), color=ft.Colors.WHITE),
        center_title=True,
        bgcolor=ft.Colors.BLUE_700,
        actions=[
            ft.PopupMenuButton(
                icon=ft.Icons.LANGUAGE,
                items=[
                    
                    ft.PopupMenuItem(text="العربية", on_click=lambda e: change_language(page, "ar", app_bar, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type, save_button, view_transactions_button, choose_type_text_control, start_date_field, end_date_field, generate_report_button, report_section_text)),
                    ft.PopupMenuItem(text="English", on_click=lambda e: change_language(page, "en", app_bar, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type, save_button, view_transactions_button, choose_type_text_control, start_date_field, end_date_field, generate_report_button, report_section_text)),
                ],
            ),
            ft.IconButton(
                icon=ft.Icons.UPLOAD_FILE,
                tooltip=translate(page, "export_csv"),
                on_click=lambda e: export_to_csv(page),
            ),
        ]
    )


    amount_field = ft.TextField(
        label=translate(page, "amount"),
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.ATTACH_MONEY,
        width=300,
        input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9.]", replacement_string=""),
        
      
    )
    category_field = ft.TextField(
        label=translate(page, "category"),
        width=300,
        prefix_icon=ft.Icons.CATEGORY,
        
    )
    description_main_field = ft.TextField(
        label=translate(page, "description_main"),
        multiline=True,
        min_lines=1,
        max_lines=2,
        width=300,
        prefix_icon=ft.Icons.DESCRIPTION,
        
    )
    description_sub_field = ft.TextField(
        label=translate(page, "description_sub"),
        width=300,
        prefix_icon=ft.Icons.SUBTITLES,
        
    )
    notes_field = ft.TextField(
        label=translate(page, "notes"),
        multiline=True,
        min_lines=1,
        max_lines=3,
        width=300,
        prefix_icon=ft.Icons.NOTES,
        
    )

    transaction_type = ft.RadioGroup(
        value="expense",
        content=ft.Row(
            [
                ft.Radio(value="income", label=translate(page, "income")),
                ft.Radio(value="expense", label=translate(page, "expense")),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        on_change=lambda e: update_input_fields_visibility(page, transaction_type, description_sub_field)
    )

    page.snack_bar = ft.SnackBar(
        ft.Text(""),
        open=False
    )

    
    view_transactions_button = ft.ElevatedButton(
        text=translate(page, "view_transactions"),
        on_click=lambda e: view_transactions_dialog(page, e),
        width=300,
        icon=ft.Icons.LIST_ALT,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        key="view_transactions_button"
    )

    
    save_button = ft.ElevatedButton(
        text=translate(page, "save"),
        on_click=lambda e: add_transaction(e, page, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type),
        width=300,
        icon=ft.Icons.SAVE,
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE,
        key="save_button"
    )

    
    start_date_field = ft.TextField(
        label=translate(page, "start_date"),
        read_only=True, 
        on_focus=lambda e: open_date_picker(e, page, start_date_field), 
        width=150,
        icon=ft.Icons.CALENDAR_MONTH,
        text_align=ft.TextAlign.CENTER,
        key="start_date_field"
    )
    end_date_field = ft.TextField(
        label=translate(page, "end_date"),
        read_only=True, 
        on_focus=lambda e: open_date_picker(e, page, end_date_field), 
        width=150,
        icon=ft.Icons.CALENDAR_MONTH,
        text_align=ft.TextAlign.CENTER,
        key="end_date_field"
    )
    report_section_text = ft.Text(translate(page, "report_section"), size=16, weight=ft.FontWeight.BOLD)
    generate_report_button = ft.ElevatedButton(
        text=translate(page, "generate_report"),
        on_click=lambda e: generate_transactions_report(page, start_date_field, end_date_field),
        width=300,
        icon=ft.Icons.PIE_CHART,
        bgcolor=ft.Colors.DEEP_PURPLE_500,
        color=ft.Colors.WHITE,
        key="generate_report_button"
    )


    
    choose_type_text_control = ft.Text(translate(page, "choose_type"), size=16, weight=ft.FontWeight.BOLD, key="choose_type_text")

    
    page.add(
        app_bar,
        ft.Column(
            [
                choose_type_text_control,
                transaction_type,
                ft.Divider(),
                amount_field,
                category_field,
                description_main_field,
                description_sub_field,
                notes_field,
                ft.Container(height=20),
                save_button,
                view_transactions_button,
                ft.Container(height=20),
                report_section_text,
                ft.Row(
                    [
                        start_date_field,
                        end_date_field,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                generate_report_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            expand=True, 
            scroll=ft.ScrollMode.ADAPTIVE 
        )
    )
    page.update()
    
    
    update_input_fields_visibility(page, transaction_type, description_sub_field)
    
    change_language(page, page.current_language, app_bar, amount_field, category_field, description_main_field, description_sub_field, notes_field, transaction_type, save_button, view_transactions_button, choose_type_text_control, start_date_field, end_date_field, generate_report_button, report_section_text)

if __name__ == "__main__":
    ft.app(main, assets_dir="assets/")