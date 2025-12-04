import os
import shutil

# Define where files SHOULD go
moves = {
    "auth": ["login.html", "register.html"],
    "admin": ["dashboard.html", "add_product.html"],
    "customer": ["home.html", "cart.html", "checkout.html", "order_history.html", "product_detail.html"],
    "root": ["base.html"]
}

base_dir = os.getcwd() # Run this from 'src'
templates_dir = os.path.join(base_dir, "app", "views", "templates")

print(f"--- Organizing Templates in {templates_dir} ---")

# Create folders
for folder in ["auth", "admin", "customer"]:
    os.makedirs(os.path.join(templates_dir, folder), exist_ok=True)

# Move files
for folder, files in moves.items():
    dest = templates_dir if folder == "root" else os.path.join(templates_dir, folder)
    for filename in files:
        # Check src folder AND templates root
        src_locs = [os.path.join(base_dir, filename), os.path.join(templates_dir, filename)]
        for src in src_locs:
            if os.path.exists(src):
                try:
                    shutil.move(src, os.path.join(dest, filename))
                    print(f"✅ Moved {filename} -> {folder}/")
                    break
                except: pass

print("🎉 Files organized. Run 'python run.py' now.")