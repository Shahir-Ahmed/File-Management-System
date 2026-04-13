# 📂 Smart File Management System

A Python-based **automatic file organizer** that monitors your Downloads folder and sorts files into categorized directories based on their extensions.

---

## 🚀 Features

- 📁 Automatically organizes downloaded files  
- 🔍 Detects file types using extensions  
- ⏳ Waits for files to fully download before processing  
- 🧠 Smart duplicate handling (renames files if needed)  
- ⚡ Real-time monitoring using file system events  
- 📝 Logging support for tracking activity  

---

## 🛠️ Tech Stack

- Python 3  
- watchdog (for real-time file monitoring)  
- pathlib (for file handling)  
- shutil (for moving files)  
- json (for rules configuration)  

---

## 📁 Project Structure

```
.
├── main.pyw              # Main script to start monitoring
├── organizer.py          # Core file organizing logic
├── rules.json            # File categorization rules
├── file_organizer.log    # Log file (generated at runtime)
└── README.md             # Project documentation
```

---

## ⚙️ How It Works

1. The script monitors your **Downloads folder**  
2. When a new file is added:  
   - It checks if the file is fully downloaded  
   - Matches its extension with predefined rules  
   - Moves it into the correct folder  
3. If no rule matches → moves to **Others**

---

## 📦 Installation

1. Clone the repository:
```bash
git clone <your-repo-link>
cd <project-folder>
```

2. Install dependencies:
```bash
pip install watchdog
```

---

## ▶️ Usage

Run the main script:

```bash
python main.pyw
```

You’ll see:

```
!!! Smart File System Active !!!
Monitoring: Downloads folder
```

Press `Ctrl + C` to stop.

---

## 🧩 Configuration

Edit `rules.json` to customize file organization:

```json
{
  "category": "Images",
  "extensions": [".jpg", ".png"],
  "target_dir": "Media/Images"
}
```

### Example Categories:

- Images → Media/Images  
- Documents → Work/Documents  
- Code → Development/Code  
- Archives → Archives  

---

## 🛡️ Safety Features

- Skips temporary files (.crdownload, .tmp, .part)  
- Waits until file is free (not in use)  
- Prevents overwriting by renaming duplicates  

---

## 📌 Future Improvements

- GUI interface  
- Custom watch folders  
- Drag-and-drop rule editor  
- File preview before moving  
- Cloud sync support  

---

## 🤝 Contributing

Feel free to fork this project and improve it. Pull requests are welcome!

---

## 📄 License

This project is open-source and available under the MIT License.