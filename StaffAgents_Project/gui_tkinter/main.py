import queue
import threading
import time
import tkinter as tk
from tkinter import filedialog, ttk


class MissionControlApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("StaffAgents Mission Control Center")
        self.root.geometry("1100x700")

        self.log_queue: "queue.Queue[str]" = queue.Queue()
        self.status_var = tk.StringVar(value="Idle")

        self._build_layout()
        self._poll_queue()

    def _build_layout(self) -> None:
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)

        # Left configuration panel
        config_frame = ttk.LabelFrame(main_frame, text="ส่วนตั้งค่าภารกิจ", padding=10)
        config_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        config_frame.columnconfigure(0, weight=1)

        ttk.Label(config_frame, text="กำหนดเป้าหมายหลัก").grid(
            row=0, column=0, sticky="w"
        )
        self.objective_text = tk.Text(config_frame, height=6, wrap="word")
        self.objective_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))

        ttk.Label(config_frame, text="เลือกโมเดลภาษา").grid(row=2, column=0, sticky="w")
        self.llm_model = ttk.Combobox(
            config_frame,
            values=["Gemini-Pro", "GPT-4o", "Claude-3-Sonnet"],
            state="readonly",
        )
        self.llm_model.current(0)
        self.llm_model.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(config_frame, text="เลือกแหล่งข้อมูล").grid(row=4, column=0, sticky="w")
        self.data_sources_var = tk.Variable(value=["Web Search", "News Feeds", "File Upload"])
        self.data_sources_listbox = tk.Listbox(
            config_frame,
            listvariable=self.data_sources_var,
            selectmode="multiple",
            height=4,
            exportselection=False,
        )
        self.data_sources_listbox.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        ttk.Label(config_frame, text="เลือกทีมปฏิบัติงาน").grid(row=6, column=0, sticky="w")
        self.agent_team = ttk.Combobox(
            config_frame,
            values=[
                "Strategic Planning Team",
                "Marketing Analysis Team",
                "Risk Assessment Team",
            ],
            state="readonly",
        )
        self.agent_team.current(0)
        self.agent_team.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        self.start_button = ttk.Button(
            config_frame, text="เริ่มภารกิจ", command=self.start_mission
        )
        self.start_button.grid(row=8, column=0, sticky="ew")

        # Right display panel
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=1, sticky="nsew")
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(2, weight=1)

        status_frame = ttk.Frame(display_frame)
        status_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ttk.Label(status_frame, text="สถานะปัจจุบัน:").pack(side="left")
        ttk.Label(status_frame, textvariable=self.status_var).pack(side="left", padx=(5, 0))

        log_frame = ttk.LabelFrame(display_frame, text="สถานะและ Log")
        log_frame.grid(row=1, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(log_frame, height=10, state="disabled", wrap="word")
        self.log_text.grid(row=0, column=0, sticky="nsew")
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        self.log_text["yscrollcommand"] = log_scroll.set

        # Notebook for reports
        notebook_frame = ttk.Frame(display_frame)
        notebook_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 0))
        notebook_frame.columnconfigure(0, weight=1)
        notebook_frame.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.summary_text = self._create_report_tab("สรุปผลผู้บริหาร")
        self.planner_text = self._create_report_tab("รายงานจากนักวางแผน")
        self.marketing_text = self._create_report_tab("รายงานจากฝ่ายการตลาด")

        button_frame = ttk.Frame(notebook_frame)
        button_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        self.export_button = ttk.Button(
            button_frame, text="Export (.md)", command=self.export_report
        )
        self.export_button.pack(side="left")

        self.translate_button = ttk.Button(
            button_frame, text="แปลเป็นภาษาไทย", command=self.translate_current_tab
        )
        self.translate_button.pack(side="left", padx=(10, 0))

    def _create_report_tab(self, title: str) -> tk.Text:
        frame = ttk.Frame(self.notebook)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        text_widget = tk.Text(frame, wrap="word")
        text_widget.grid(row=0, column=0, sticky="nsew")
        text_widget.insert("1.0", "ยังไม่มีรายงาน")
        self.notebook.add(frame, text=title)
        return text_widget

    def start_mission(self) -> None:
        if hasattr(self, "worker_thread") and self.worker_thread.is_alive():
            return

        self.status_var.set("Running...")
        self._clear_logs()
        self._clear_reports()

        self.worker_thread = threading.Thread(target=self._simulate_workflow, daemon=True)
        self.worker_thread.start()

    def _simulate_workflow(self) -> None:
        sample_logs = [
            "[Manager]: กำลังมอบหมายงานให้ทีม...",
            "[Planner]: กำลังค้นหาข้อมูลยุทธศาสตร์...",
            "[Analyst]: ประเมินความเสี่ยงจากฐานข้อมูล...",
            "[Marketing]: รวบรวมแนวโน้มตลาดจากข่าว...",
            "[Researcher]: ตรวจสอบความถูกต้องของข้อมูล...",
            "[Planner]: สรุปข้อมูลเพื่อนำเสนอ...",
            "[Manager]: ตรวจสอบความครบถ้วนของรายงาน...",
        ]
        for entry in sample_logs:
            self.log_queue.put(entry)
            time.sleep(1)

        objective = self.objective_text.get("1.0", "end").strip() or "ยังไม่ได้กำหนด"
        summary_content = (
            "# ภาพรวมภารกิจ\n\n"
            "## เป้าหมายหลัก\n"
            f"- {objective}\n\n"
            "## ไฮไลต์สำคัญ\n"
            "- ทีมงานรวบรวมข้อมูลจากแหล่งที่เกี่ยวข้อง\n"
            "- วิเคราะห์โอกาสและความเสี่ยงเชิงกลยุทธ์\n"
            "- เตรียมข้อเสนอแนะสำหรับผู้บริหาร\n"
        )
        planner_content = (
            "# รายงานจากนักวางแผน\n\n"
            "- ประมวลผลข้อมูลยุทธศาสตร์หลัก\n"
            "- จัดลำดับความสำคัญของโครงการ\n"
            "- เตรียมแผนตอบสนองตามสถานการณ์\n"
        )
        marketing_content = (
            "# รายงานจากฝ่ายการตลาด\n\n"
            "- วิเคราะห์แนวโน้มตลาดล่าสุด\n"
            "- ประเมินคู่แข่งหลัก\n"
            "- จัดทำแผนการสื่อสารเชิงรุก\n"
        )

        self.log_queue.put(("reports", summary_content, planner_content, marketing_content))
        self.log_queue.put(("status", "Complete"))

    def _poll_queue(self) -> None:
        try:
            while True:
                item = self.log_queue.get_nowait()
                if isinstance(item, tuple):
                    if item[0] == "reports":
                        self._update_report(self.summary_text, item[1])
                        self._update_report(self.planner_text, item[2])
                        self._update_report(self.marketing_text, item[3])
                    elif item[0] == "status":
                        self.status_var.set(item[1])
                else:
                    self._append_log(item)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._poll_queue)

    def _append_log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        current_text = self.log_text.get("1.0", "end").strip()
        if current_text == "ยังไม่มีข้อมูล Log" or not current_text:
            self.log_text.delete("1.0", "end")
        self.log_text.insert("end", message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def _clear_logs(self) -> None:
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.insert("1.0", "กำลังเตรียมเริ่มภารกิจ...")
        self.log_text.configure(state="disabled")

    def _clear_reports(self) -> None:
        for widget in (self.summary_text, self.planner_text, self.marketing_text):
            widget.delete("1.0", "end")
            widget.insert("1.0", "ยังไม่มีรายงาน")

    def _update_report(self, widget: tk.Text, content: str) -> None:
        widget.delete("1.0", "end")
        widget.insert("1.0", content)

    def translate_current_tab(self) -> None:
        current_tab = self.notebook.select()
        widget = self.root.nametowidget(current_tab)
        text_widget = widget.winfo_children()[0]
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", "นี่คือรายงานฉบับแปลภาษาไทย (ตัวอย่าง)")

    def export_report(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")],
            title="บันทึกสรุปผลผู้บริหาร",
        )
        if not file_path:
            return

        content = self.summary_text.get("1.0", "end").strip()
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


def main() -> None:
    root = tk.Tk()
    MissionControlApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
