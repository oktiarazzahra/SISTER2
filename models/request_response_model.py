from models.common import Packet


class RequestResponseModel:
    """Model sinkron: request dari client lalu response kembali ke client."""

    model_name = "request-response"

    def emit_event(self, sim, msg_id: int) -> None:
        """Buat paket request awal dari Sensor menuju Service lewat Gateway."""
        sim.metrics[self.model_name]["total"] += 1
        sim._push_seq(self.model_name, f"#{msg_id}:REQ")

        path = [
            (sim.nodes["sensor"].x, sim.nodes["sensor"].y),
            (sim.nodes["gateway"].x, sim.nodes["gateway"].y),
            (sim.nodes["service"].x, sim.nodes["service"].y),
        ]
        packet = Packet(msg_id, self.model_name, "request", "event", path, 1.8, sim.sim_time)

        if sim._drop():
            packet.dropped = True
            packet.kind = "drop"
            sim.metrics[self.model_name]["dropped"] += 1
            sim._log(f"RR #{msg_id} drop di jalur Sensor -> Gateway")
        else:
            sim._log(f"RR #{msg_id} request dikirim")
        sim.packets.append(packet)

    def on_arrive(self, sim, packet: Packet) -> None:
        """Saat request tiba buat response, saat response tiba catat latensi."""
        if packet.phase == "request":
            path = [
                (sim.nodes["service"].x, sim.nodes["service"].y),
                (sim.nodes["gateway"].x, sim.nodes["gateway"].y),
                (sim.nodes["dashboard"].x, sim.nodes["dashboard"].y),
            ]
            response_packet = Packet(
                packet.msg_id,
                self.model_name,
                "response",
                "response",
                path,
                1.7,
                sim.sim_time,
            )
            sim.packets.append(response_packet)
        elif packet.phase == "response":
            latency = (sim.sim_time - packet.created_at) * 1000.0
            sim.metrics[self.model_name]["delivered"] += 1
            sim.metrics[self.model_name]["latency_sum"] += latency
            sim._log(f"RR #{packet.msg_id} selesai, response diterima")
