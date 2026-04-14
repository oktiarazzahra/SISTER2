from models.common import Packet


class MessagePassingModel:
    """Model pipeline: pesan bergerak bertahap antar komponen pemrosesan."""

    model_name = "message-passing"

    def emit_event(self, sim, msg_id: int) -> None:
        """Kirim pesan awal dari Sensor ke Broker (queue entry)."""
        sim.metrics[self.model_name]["total"] += 1
        sim._push_seq(self.model_name, f"#{msg_id}:MSG")

        path = [
            (sim.nodes["sensor"].x, sim.nodes["sensor"].y),
            (sim.nodes["broker"].x, sim.nodes["broker"].y),
        ]
        packet = Packet(msg_id, self.model_name, "send", "event", path, 2.0, sim.sim_time)

        if sim._drop():
            packet.dropped = True
            packet.kind = "drop"
            sim.metrics[self.model_name]["dropped"] += 1
            sim._log(f"MP #{msg_id} drop di jalur Sensor -> Broker")
        else:
            sim._log(f"MP #{msg_id} message dikirim ke antrean")

        sim.packets.append(packet)

    def on_arrive(self, sim, packet: Packet) -> None:
        """Lanjutkan alur send -> route -> consume dan akhiri dengan metrik latency."""
        if packet.phase == "send":
            path = [
                (sim.nodes["broker"].x, sim.nodes["broker"].y),
                (sim.nodes["service"].x, sim.nodes["service"].y),
            ]
            route_packet = Packet(packet.msg_id, self.model_name, "route", "event", path, 2.0, sim.sim_time)
            sim.packets.append(route_packet)
        elif packet.phase == "route":
            path = [
                (sim.nodes["service"].x, sim.nodes["service"].y),
                (sim.nodes["dashboard"].x, sim.nodes["dashboard"].y),
            ]
            consume_packet = Packet(packet.msg_id, self.model_name, "consume", "response", path, 1.8, sim.sim_time)
            if sim._drop():
                consume_packet.dropped = True
                consume_packet.kind = "drop"
                sim.metrics[self.model_name]["dropped"] += 1
                sim._log(f"MP #{packet.msg_id} drop di jalur Service -> Dashboard")
            sim.packets.append(consume_packet)
        elif packet.phase == "consume":
            latency = (sim.sim_time - packet.created_at) * 1000.0
            sim.metrics[self.model_name]["delivered"] += 1
            sim.metrics[self.model_name]["latency_sum"] += latency
            sim._log(f"MP #{packet.msg_id} message diproses di Dashboard")
