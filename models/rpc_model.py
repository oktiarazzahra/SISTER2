from models.common import Packet


class RPCModel:
    model_name = "rpc"

    def emit_event(self, sim, msg_id: int) -> None:
        sim.metrics[self.model_name]["total"] += 1
        sim._push_seq(self.model_name, f"#{msg_id}:CALL")

        path = [
            (sim.nodes["sensor"].x, sim.nodes["sensor"].y),
            (sim.nodes["gateway"].x, sim.nodes["gateway"].y),
            (sim.nodes["service"].x, sim.nodes["service"].y),
        ]
        packet = Packet(msg_id, self.model_name, "call", "event", path, 2.1, sim.sim_time)

        if sim._drop():
            packet.dropped = True
            packet.kind = "drop"
            sim.metrics[self.model_name]["dropped"] += 1
            sim._log(f"RPC #{msg_id} call gagal di jaringan")
        else:
            sim._log(f"RPC #{msg_id} call dikirim")

        sim.packets.append(packet)

    def on_arrive(self, sim, packet: Packet) -> None:
        if packet.phase == "call":
            path = [
                (sim.nodes["service"].x, sim.nodes["service"].y),
                (sim.nodes["gateway"].x, sim.nodes["gateway"].y),
                (sim.nodes["sensor"].x, sim.nodes["sensor"].y),
            ]
            result_packet = Packet(packet.msg_id, self.model_name, "result", "response", path, 1.9, sim.sim_time)
            if sim._drop():
                result_packet.dropped = True
                result_packet.kind = "drop"
                sim.metrics[self.model_name]["dropped"] += 1
                sim._log(f"RPC #{packet.msg_id} response gagal kembali ke caller")
            sim.packets.append(result_packet)
        elif packet.phase == "result":
            latency = (sim.sim_time - packet.created_at) * 1000.0
            sim.metrics[self.model_name]["delivered"] += 1
            sim.metrics[self.model_name]["latency_sum"] += latency
            sim._log(f"RPC #{packet.msg_id} selesai, hasil diterima caller")
