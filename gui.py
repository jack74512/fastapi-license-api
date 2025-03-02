import tkinter as tk
from tkinter import messagebox
import requests
import uuid
import platform
import subprocess

# 🔹 استخراج UUID تلقائيًا من الجهاز
def get_device_uuid():
    try:
        if platform.system() == "Windows":
            # استخدام wmic لجلب UUID
            output = subprocess.check_output("wmic csproduct get uuid", shell=True).decode().split("\n")[1].strip()
            if output:
                return output
        elif platform.system() == "Linux":
            # استخدام cat لجلب UUID على Linux
            output = subprocess.check_output("cat /var/lib/dbus/machine-id", shell=True).decode().strip()
            if output:
                return output
        elif platform.system() == "Darwin":
            # macOS: استخدام system_profiler لجلب UUID
            output = subprocess.check_output("system_profiler SPHardwareDataType | awk '/UUID/ {print $3}'", shell=True).decode().strip()
            if output:
                return output
    except:
        pass

    # إذا فشلت كل المحاولات، يتم توليد UUID عشوائي
    return str(uuid.uuid4())

# 🔹 إرسال الطلب إلى FastAPI
def check_license():
    license_key = license_entry.get().strip()
    
    if not license_key:
        messagebox.showerror("Error", "Please enter a license key")
        return

    device_uuid = get_device_uuid()
    api_url = "https://your-fastapi-url.onrender.com/verify-license/"
    
    try:
        response = requests.post(api_url, params={"license_key": license_key, "uuid": device_uuid})
        data = response.json()

        if response.status_code == 200:
            messagebox.showinfo("Success", data["message"])
        else:
            messagebox.showerror("Error", data["detail"])

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Connection failed: {str(e)}")

# 🔹 إنشاء نافذة GUI باستخدام Tkinter
root = tk.Tk()
root.title("License Verification")
root.geometry("400x250")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# 🔹 إضافة عنوان التطبيق
title_label = tk.Label(root, text="🔑 License Verification", font=("Arial", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=15)

# 🔹 حقل إدخال مفتاح التفعيل
tk.Label(root, text="Enter your License Key:", font=("Arial", 12), bg="#f0f0f0").pack()
license_entry = tk.Entry(root, font=("Arial", 12), width=30, justify="center")
license_entry.pack(pady=5)
license_entry.focus()

# 🔹 زر التحقق من المفتاح
check_button = tk.Button(root, text="Verify License", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", width=20, command=check_license)
check_button.pack(pady=15)

# 🔹 إضافة وظيفة لاستخدام زر `Enter` للتحقق من المفتاح
root.bind("<Return>", lambda event: check_license())

# 🔹 تشغيل النافذة
root.mainloop()
