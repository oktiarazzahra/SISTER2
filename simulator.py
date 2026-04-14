import time
import tkinter as tk
from typing import Dict, List, Optional, Tuple

from models.common import Node, Packet
from models.message_passing_model import MessagePassingModel
from models.publish_subscribe_model import PublishSubscribeModel
from models.request_response_model import RequestResponseModel


class DistributedCommSimulator:
    """Simulator utama: mengatur UI, loop waktu, paket, dan metrik komparatif."""

    model_order = [
        "request-response",
        "publish-subscribe",
        "message-passing",
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simulasi Model Komunikasi - Sistem Terdistribusi (Python Tkinter)")
        self.root.geometry("1220x760")
        self.root.minsize(1100, 700)

        self.running = False
        self.loss_mode = False
        self.last_tick = time.perf_counter()
        self.sim_time = 0.0
        self.accumulator = 0.0
        self.next_id = 1

        self.model_var = tk.StringVar(value="request-response")
        self.rate_var = tk.IntVar(value=2)
        self.sub_var = tk.IntVar(value=3)

        self.metrics: Dict[str, Dict[str, object]] = self._new_metrics()

        self.packets: List[Packet] = []
        self.subscribers: List[Node] = []

        self.nodes = {
            "sensor": Node("Sensor", 130, 280, "#1d3557"),
            "gateway": Node("Gateway", 340, 170, "#264653"),
            "service": Node("Service", 550, 280, "#0b7285"),
            "broker": Node("Broker", 550, 90, "#2a9d8f"),
            "dashboard": Node("Dashboard", 790, 170, "#457b9d"),
        }

        self.rr_model = RequestResponseModel()
        self.ps_model = PublishSubscribeModel()
        self.mp_model = MessagePassingModel()

        self._build_ui()
        self._rebuild_subscribers()
        self._render_scene()
        self._loop()

    def _build_ui(self) -> None:
        self.root.configure(bg="#f2f5f7")

        title = tk.Label(
            self.root,
            text="Simulasi Interaktif Model Komunikasi Sistem Terdistribusi",
            font=("Segoe UI", 16, "bold"),
            bg="#f2f5f7",
            fg="#0f1720",
        )
        title.pack(anchor="w", padx=12, pady=(12, 6))

        wrapper = tk.Frame(self.root, bg="#f2f5f7")
        wrapper.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        left = tk.Frame(wrapper, bg="#ffffff", bd=1, relief="solid")
        left.pack(side="left", fill="y")

        right = tk.Frame(wrapper, bg="#f2f5f7")
        right.pack(side="left", fill="both", expand=True, padx=(12, 0))

        self._build_controls(left)
        self._build_visual(right)
        self._build_bottom(right)

    def _build_controls(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="Kontrol", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(
            anchor="w", padx=10, pady=(10, 8)
        )

        tk.Label(parent, text="Model Komunikasi", bg="#ffffff", anchor="w").pack(
            fill="x", padx=10
        )
        model_menu = tk.OptionMenu(
            parent,
            self.model_var,
            "request-response",
            "publish-subscribe",
            "message-passing",
            command=lambda _: self._log("Model diubah: " + self.model_var.get()),
        )
        model_menu.config(width=20)
        model_menu.pack(fill="x", padx=10, pady=(2, 8))

        tk.Label(parent, text="Laju Event / detik", bg="#ffffff", anchor="w").pack(
            fill="x", padx=10
        )
        tk.Scale(
            parent,
            from_=1,
            to=10,
            orient="horizontal",
            variable=self.rate_var,
            bg="#ffffff",
            highlightthickness=0,
            relief="flat",
        ).pack(fill="x", padx=10, pady=(2, 8))

        tk.Label(parent, text="Jumlah Subscriber (Pub-Sub)", bg="#ffffff", anchor="w").pack(
            fill="x", padx=10
        )
        tk.Scale(
            parent,
            from_=1,
            to=8,
            orient="horizontal",
            variable=self.sub_var,
            bg="#ffffff",
            highlightthickness=0,
            relief="flat",
            command=lambda _: self._rebuild_subscribers(),
        ).pack(fill="x", padx=10, pady=(2, 10))

        btn_wrap = tk.Frame(parent, bg="#ffffff")
        btn_wrap.pack(fill="x", padx=10, pady=(2, 6))

        tk.Button(btn_wrap, text="Mulai", command=self.start, bg="#005f73", fg="white").pack(
            fill="x", pady=2
        )
        tk.Button(btn_wrap, text="Jeda", command=self.stop, bg="#6c757d", fg="white").pack(
            fill="x", pady=2
        )
        tk.Button(btn_wrap, text="Kirim 1 Event", command=self.step_once).pack(fill="x", pady=2)
        tk.Button(btn_wrap, text="Burst 20", command=self.burst).pack(fill="x", pady=2)
        tk.Button(btn_wrap, text="Reset", command=self.reset, bg="#b42318", fg="white").pack(
            fill="x", pady=2
        )

        self.loss_btn = tk.Button(parent, text="Simulasi Gangguan: OFF", command=self.toggle_loss)
        self.loss_btn.pack(fill="x", padx=10, pady=(8, 10))

        self.clock_label = tk.Label(
            parent,
            text="t = 0.0s",
            bg="#ffffff",
            fg="#475569",
            font=("Consolas", 10),
        )
        self.clock_label.pack(anchor="w", padx=10, pady=(0, 10))

    def _build_visual(self, parent: tk.Frame) -> None:
        top = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid")
        top.pack(fill="both", expand=True)

        tk.Label(top, text="Visualisasi Aliran Pesan", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=10, pady=(8, 4)
        )

        self.canvas = tk.Canvas(top, width=860, height=430, bg="#f9fcff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _build_bottom(self, parent: tk.Frame) -> None:
        bottom = tk.Frame(parent, bg="#f2f5f7")
        bottom.pack(fill="both", expand=False, pady=(10, 0))

        metrics_card = tk.Frame(bottom, bg="#ffffff", bd=1, relief="solid")
        metrics_card.pack(side="left", fill="both", expand=True)

        tk.Label(metrics_card, text="Metrik Perbandingan", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=10, pady=(8, 4)
        )

        self.metrics_text = tk.Text(metrics_card, height=11, bg="#ffffff", relief="flat", wrap="word")
        self.metrics_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        log_card = tk.Frame(bottom, bg="#ffffff", bd=1, relief="solid")
        log_card.pack(side="left", fill="both", expand=True, padx=(10, 0))

        tk.Label(log_card, text="Log Peristiwa", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", padx=10, pady=(8, 4)
        )

        self.log_text = tk.Text(
            log_card,
            height=11,
            bg="#0f1720",
            fg="#dbeafe",
            relief="flat",
            wrap="none",
            font=("Consolas", 9),
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _rebuild_subscribers(self) -> None:
        self.subscribers.clear()
        count = int(self.sub_var.get())
        y0 = 230
        for i in range(count):
            self.subscribers.append(Node(f"Sub-{i + 1}", 790, y0 + (i * 36), "#6c8ebf", radius=18))
        self._render_scene()

    def _new_metrics(self) -> Dict[str, Dict[str, object]]:
        """Inisialisasi metrik per model agar reset dan startup konsisten."""
        metrics: Dict[str, Dict[str, object]] = {}
        for model in self.model_order:
            metrics[model] = {
                "total": 0,
                "delivered": 0,
                "dropped": 0,
                "latency_sum": 0.0,
                "seq": [],
            }
        return metrics

    def _log(self, text: str) -> None:
        line = f"[{self.sim_time:6.2f}s] {text}\n"
        self.log_text.insert("1.0", line)
        self.log_text.delete("140.0", "end")

    def _drop(self) -> bool:
        from random import random

        return self.loss_mode and random() < 0.17

    def _push_seq(self, model: str, value: str) -> None:
        seq = self.metrics[model]["seq"]
        if isinstance(seq, list):
            seq.append(value)
            if len(seq) > 8:
                seq.pop(0)

    def emit_event(self, forced_model: Optional[str] = None) -> None:
        """Dispatch event ke implementasi model aktif."""
        model = forced_model or self.model_var.get()
        msg_id = self.next_id
        self.next_id += 1

        if model == "request-response":
            self.rr_model.emit_event(self, msg_id)
        elif model == "publish-subscribe":
            self.ps_model.emit_event(self, msg_id)
        else:
            self.mp_model.emit_event(self, msg_id)

    def _arrive(self, packet: Packet) -> None:
        """Teruskan paket yang tiba ke handler model sesuai jenis paket."""
        if packet.dropped:
            return

        if packet.model == "request-response":
            self.rr_model.on_arrive(self, packet)
        elif packet.model == "publish-subscribe":
            self.ps_model.on_arrive(self, packet)
        else:
            self.mp_model.on_arrive(self, packet)

    def _update_packets(self, dt: float) -> None:
        """Gerakkan paket dan proses paket yang sudah mencapai ujung jalur."""
        alive: List[Packet] = []
        for p in self.packets:
            segs = len(p.path) - 1
            if segs <= 0:
                continue

            p.progress += (p.speed * dt)
            if p.progress >= segs:
                self._arrive(p)
                continue
            alive.append(p)
        self.packets = alive

    def _packet_pos(self, p: Packet) -> Tuple[float, float]:
        idx = int(p.progress)
        t = p.progress - idx
        x1, y1 = p.path[idx]
        x2, y2 = p.path[idx + 1]
        return x1 + (x2 - x1) * t, y1 + (y2 - y1) * t

    def _draw_node(self, node: Node) -> None:
        x, y, r = node.x, node.y, node.radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=node.color, outline="")
        self.canvas.create_text(x, y, text=node.name, fill="white", font=("Segoe UI", 9, "bold"))

    def _draw_edge(self, a: Node, b: Node, dashed: bool = False) -> None:
        self.canvas.create_line(
            a.x,
            a.y,
            b.x,
            b.y,
            fill="#9bb0c4",
            width=2,
            dash=(5, 4) if dashed else None,
        )

    def _render_scene(self) -> None:
        """Render node, edge, dan paket aktif untuk model yang sedang dipilih."""
        self.canvas.delete("all")

        model = self.model_var.get()
        if model == "request-response":
            self._draw_edge(self.nodes["sensor"], self.nodes["gateway"])
            self._draw_edge(self.nodes["gateway"], self.nodes["service"])
            self._draw_edge(self.nodes["service"], self.nodes["gateway"], dashed=True)
            self._draw_edge(self.nodes["gateway"], self.nodes["dashboard"], dashed=True)

            self._draw_node(self.nodes["sensor"])
            self._draw_node(self.nodes["gateway"])
            self._draw_node(self.nodes["service"])
            self._draw_node(self.nodes["dashboard"])
        elif model == "publish-subscribe":
            self._draw_edge(self.nodes["sensor"], self.nodes["broker"])
            for sub in self.subscribers:
                self._draw_edge(self.nodes["broker"], sub)

            self._draw_node(self.nodes["sensor"])
            self._draw_node(self.nodes["broker"])
            for sub in self.subscribers:
                self._draw_node(sub)
        elif model == "message-passing":
            self._draw_edge(self.nodes["sensor"], self.nodes["broker"])
            self._draw_edge(self.nodes["broker"], self.nodes["service"])
            self._draw_edge(self.nodes["service"], self.nodes["dashboard"])

            self._draw_node(self.nodes["sensor"])
            self._draw_node(self.nodes["broker"])
            self._draw_node(self.nodes["service"])
            self._draw_node(self.nodes["dashboard"])

        for p in self.packets:
            x, y = self._packet_pos(p)
            color = "#0a9396"
            if p.kind == "response":
                color = "#ca6702"
            if p.kind == "drop":
                color = "#b42318"
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill=color, outline="")

        self.canvas.create_text(
            14,
            14,
            anchor="nw",
            text="Legenda: Event(hijau) | Response(oranye) | Drop(merah)",
            fill="#475569",
            font=("Segoe UI", 9),
        )

    def _update_metrics_view(self) -> None:
        """Hitung throughput/latensi tiap model lalu tampilkan analisis singkat."""
        elapsed = max(self.sim_time, 1e-6)

        lines: List[str] = []
        throughput_by_model: Dict[str, float] = {}
        latency_by_model: Dict[str, float] = {}

        for model in self.model_order:
            stats = self.metrics[model]
            throughput = stats["delivered"] / elapsed
            avg_latency = stats["latency_sum"] / stats["delivered"] if stats["delivered"] else 0.0
            sequence = " | ".join(stats["seq"]) if stats["seq"] else "-"

            throughput_by_model[model] = throughput
            latency_by_model[model] = avg_latency

            lines.extend(
                [
                    f"{model.upper()}",
                    f"- Total pesan: {stats['total']}",
                    f"- Throughput: {throughput:.2f} msg/s",
                    f"- Rata-rata latensi: {avg_latency:.2f} ms",
                    f"- Drop: {stats['dropped']}",
                    f"- Urutan terakhir: {sequence}",
                    "",
                ]
            )

        thr_winner = max(throughput_by_model, key=throughput_by_model.get)
        delivered_models = [m for m in self.model_order if self.metrics[m]["delivered"] > 0]
        lat_winner = min(delivered_models, key=lambda m: latency_by_model[m]) if delivered_models else "belum-ada-data"

        lines.extend(
            [
                "ANALISIS OTOMATIS",
                f"- Throughput unggul: {thr_winner}",
                f"- Latensi unggul: {lat_winner}",
                "- Request-Response cocok untuk pola call-return.",
                "- Publish-Subscribe cocok untuk fanout event.",
                "- Message-Passing cocok untuk pipeline antar komponen.",
            ]
        )

        text = "\n".join(lines)

        self.metrics_text.delete("1.0", "end")
        self.metrics_text.insert("1.0", text)

    def _loop(self) -> None:
        """Main loop simulasi: update waktu, generate event, update render+metrik."""
        now = time.perf_counter()
        dt = now - self.last_tick
        self.last_tick = now

        if self.running:
            self.sim_time += dt
            self.accumulator += dt
            interval = 1.0 / max(1, int(self.rate_var.get()))

            while self.accumulator >= interval:
                self.emit_event()
                self.accumulator -= interval

            self._update_packets(dt)

        self.clock_label.config(text=f"t = {self.sim_time:.1f}s")
        self._render_scene()
        self._update_metrics_view()
        self.root.after(16, self._loop)

    def start(self) -> None:
        self.running = True
        self._log("Simulasi dimulai")

    def stop(self) -> None:
        self.running = False
        self._log("Simulasi dijeda")

    def step_once(self) -> None:
        self.emit_event()
        self._update_packets(0.04)
        self._render_scene()
        self._update_metrics_view()

    def burst(self) -> None:
        for _ in range(20):
            self.emit_event()
        self._log("Burst 20 event dikirim")

    def toggle_loss(self) -> None:
        self.loss_mode = not self.loss_mode
        if self.loss_mode:
            self.loss_btn.config(text="Simulasi Gangguan: ON", bg="#b42318", fg="white")
            self._log("Mode gangguan aktif")
        else:
            self.loss_btn.config(text="Simulasi Gangguan: OFF", bg="SystemButtonFace", fg="black")
            self._log("Mode gangguan nonaktif")

    def reset(self) -> None:
        self.running = False
        self.loss_mode = False
        self.loss_btn.config(text="Simulasi Gangguan: OFF", bg="SystemButtonFace", fg="black")

        self.sim_time = 0.0
        self.accumulator = 0.0
        self.next_id = 1
        self.packets.clear()
        self.log_text.delete("1.0", "end")

        self.metrics = self._new_metrics()
        self._log("Simulasi direset")


def main() -> None:
    root = tk.Tk()
    DistributedCommSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
