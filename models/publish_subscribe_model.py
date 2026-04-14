from models.common import Packet


class PublishSubscribeModel:
    """Model event-driven: publisher kirim ke broker lalu fanout ke subscriber."""

    model_name = "publish-subscribe"

    def emit_event(self, sim, msg_id: int) -> None:
        """Publish event dari Sensor ke Broker sebagai titik fanout."""
        fanout = max(1, len(sim.subscribers))
        sim.metrics[self.model_name]["total"] += fanout
        sim._push_seq(self.model_name, f"#{msg_id}:PUBx{fanout}")

        path = [
            (sim.nodes["sensor"].x, sim.nodes["sensor"].y),
            (sim.nodes["broker"].x, sim.nodes["broker"].y),
        ]
        packet = Packet(msg_id, self.model_name, "publish", "event", path, 2.1, sim.sim_time)
        sim.packets.append(packet)
        sim._log(f"PS #{msg_id} publish ke Broker (fanout={fanout})")

    def on_arrive(self, sim, packet: Packet) -> None:
        """Saat publish tiba lakukan fanout, saat deliver tiba catat latensi."""
        if packet.phase == "publish":
            for subscriber in sim.subscribers:
                path = [
                    (sim.nodes["broker"].x, sim.nodes["broker"].y),
                    (subscriber.x, subscriber.y),
                ]
                delivery_packet = Packet(
                    packet.msg_id,
                    self.model_name,
                    "deliver",
                    "response",
                    path,
                    2.3,
                    sim.sim_time,
                )
                if sim._drop():
                    delivery_packet.dropped = True
                    delivery_packet.kind = "drop"
                    sim.metrics[self.model_name]["dropped"] += 1
                    sim._log(f"PS #{packet.msg_id} drop ke {subscriber.name}")
                sim.packets.append(delivery_packet)
        elif packet.phase == "deliver":
            latency = (sim.sim_time - packet.created_at) * 1000.0
            sim.metrics[self.model_name]["delivered"] += 1
            sim.metrics[self.model_name]["latency_sum"] += latency
