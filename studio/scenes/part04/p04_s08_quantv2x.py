"""P04-S08: QuantV2X quantizes both the model and the V2X message."""
from manimlib import *

from studio.components import (
    StudioScene, BG_PAPER, PASTEL_BLUE, PASTEL_GREEN, PASTEL_AMBER,
    RED_ERROR, GREEN_FIX, ACCENT_BLUE, ACCENT_TEAL, ACCENT_AMBER,
    GOLD_RICH, INK_DARK, INK_MID,
    FONT_PRIMARY, SIZE_LABEL, SIZE_CAPS,
    vehicle_icon,
)

SCRIPT = (
    "QuantV2X is fully quantized at two levels. First, the complete perception "
    "network moves from FP32 to INT8. Second, BEV features are represented as "
    "low-bit code indices, making the V2X payload three hundred times smaller."
)


def label(text, size=SIZE_LABEL, color=INK_DARK, weight=NORMAL):
    mob = Text(text, font=FONT_PRIMARY, font_size=size, weight=weight)
    mob.set_color(color)
    return mob


def number_badge(number, color):
    circle = Circle(radius=0.16)
    circle.set_fill(color, opacity=1.0)
    circle.set_stroke(color, width=0)
    number_text = label(str(number), SIZE_CAPS - 1, WHITE, BOLD)
    number_text.move_to(circle)
    return VGroup(circle, number_text)


def network_row(color, precision):
    modules = VGroup()
    for name, width in [("Encoder", 1.35), ("Fusion", 1.2), ("Head", 1.05)]:
        box = RoundedRectangle(width=width, height=0.72, corner_radius=0.1)
        box.set_fill(color, opacity=0.1)
        box.set_stroke(color, width=1.7, opacity=0.9)
        name_text = label(name, SIZE_CAPS - 1, INK_DARK, BOLD)
        precision_text = label(precision, SIZE_CAPS - 3, color, BOLD)
        copy = VGroup(name_text, precision_text)
        copy.arrange(DOWN, buff=0.08)
        copy.move_to(box)
        modules.add(VGroup(box, copy))
    modules.arrange(RIGHT, buff=0.17)
    return modules


def feature_tensor(color=ACCENT_BLUE, *, rows=4, cols=6, cell=0.24):
    layers = VGroup()
    palette = [color, ACCENT_TEAL, ACCENT_AMBER]
    for layer_index, layer_color in enumerate(palette):
        grid = VGroup()
        for row in range(rows):
            for col in range(cols):
                square = Square(side_length=cell)
                square.set_fill(layer_color, opacity=0.13 + 0.04 * layer_index)
                square.set_stroke(layer_color, width=0.8, opacity=0.48)
                square.move_to([
                    (col - (cols - 1) / 2) * cell,
                    (row - (rows - 1) / 2) * cell,
                    0,
                ])
                grid.add(square)
        grid.shift(UP * 0.08 * layer_index + RIGHT * 0.1 * layer_index)
        layers.add(grid)
    return layers


def codebook():
    colors = [ACCENT_BLUE, "#8B5CF6", ACCENT_TEAL, GREEN_FIX, ACCENT_AMBER]
    swatches = VGroup()
    for index, color in enumerate(colors):
        swatch = RoundedRectangle(width=0.34, height=0.94, corner_radius=0.05)
        swatch.set_fill(color, opacity=0.28)
        swatch.set_stroke(color, width=1.2, opacity=0.75)
        index_text = label(str(index), SIZE_CAPS - 3, color, BOLD)
        index_text.move_to(swatch)
        swatches.add(VGroup(swatch, index_text))
    swatches.arrange(RIGHT, buff=0.04)
    return swatches


def index_packet(rows=3, cols=5, cell=0.2):
    colors = [ACCENT_BLUE, "#8B5CF6", ACCENT_TEAL, GREEN_FIX, ACCENT_AMBER]
    values = [0, 2, 1, 4, 3, 1, 1, 3, 2, 0, 4, 2, 3, 0, 1]
    cells = VGroup()
    for index, value in enumerate(values):
        row, col = divmod(index, cols)
        square = Square(side_length=cell)
        square.set_fill(colors[value], opacity=0.72)
        square.set_stroke(BG_PAPER, width=0.8, opacity=1.0)
        square.move_to([
            (col - (cols - 1) / 2) * cell,
            ((rows - 1) / 2 - row) * cell,
            0,
        ])
        cells.add(square)
    frame = RoundedRectangle(
        width=cols * cell + 0.18,
        height=rows * cell + 0.18,
        corner_radius=0.08,
    )
    frame.set_fill(BG_PAPER, opacity=0.15)
    frame.set_stroke(GREEN_FIX, width=1.8, opacity=0.95)
    return VGroup(frame, cells)


class P04S08QuantV2X(StudioScene):
    PART_NUM = 4
    SCENE_TITLE = "QuantV2X: Fully Quantized V2X"

    def construct(self):
        self.camera.background_color = BG_PAPER
        self._open(self.SCENE_TITLE)

        # Layer 1: concise, model-level conversion.
        layer1_badge = number_badge(1, ACCENT_BLUE)
        layer1_title = label("MODEL QUANTIZATION", SIZE_LABEL, INK_DARK, BOLD)
        layer1_sub = label("every perception block", SIZE_CAPS, INK_MID)
        layer1_copy = VGroup(layer1_title, layer1_sub)
        layer1_copy.arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        layer1_heading = VGroup(layer1_badge, layer1_copy)
        layer1_badge.move_to([-6.72, 2.12, 0])
        layer1_copy.next_to(layer1_badge, RIGHT, buff=0.12)

        fp_model = network_row(RED_ERROR, "FP32")
        int_model = network_row(GREEN_FIX, "INT8")
        fp_model.scale(0.82).move_to(LEFT * 2.65 + UP * 1.5)
        int_model.scale(0.82).move_to(RIGHT * 2.65 + UP * 1.5)

        quant_arrow = Arrow(
            [-0.75, 1.5, 0],
            [0.75, 1.5, 0],
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        quant_arrow.set_stroke(INK_MID, width=2.1, opacity=0.8)
        quant_arrow.set_fill(INK_MID, opacity=0.8)
        quant_text = label("POST-TRAINING\nQUANTIZATION", SIZE_CAPS - 2, INK_MID, BOLD)
        quant_text.next_to(quant_arrow, UP, buff=0.2)
        memory_note = label("4x smaller model memory", SIZE_CAPS, GREEN_FIX, BOLD)
        memory_note.next_to(int_model, DOWN, buff=0.1)

        self.play(FadeIn(layer1_heading), FadeIn(fp_model), run_time=0.95)
        self.play(ShowCreation(quant_arrow), FadeIn(quant_text), run_time=0.7)
        self.play(
            TransformFromCopy(fp_model, int_model),
            FadeIn(memory_note, shift=0.08 * UP),
            run_time=1.2,
        )

        # Layer 2: the actual cooperative message, following the source diagram.
        layer2_badge = number_badge(2, ACCENT_TEAL)
        layer2_title = label("MESSAGE QUANTIZATION", SIZE_LABEL, INK_DARK, BOLD)
        layer2_sub = label("feature tensor  \u2192  code indices  \u2192  reconstruction", SIZE_CAPS, INK_MID)
        layer2_copy = VGroup(layer2_title, layer2_sub)
        layer2_copy.arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        layer2_heading = VGroup(layer2_badge, layer2_copy)
        layer2_badge.move_to([-6.72, 0.55, 0])
        layer2_copy.next_to(layer2_badge, RIGHT, buff=0.12)
        self.play(FadeIn(layer2_heading), run_time=0.4)

        sender_car = vehicle_icon(color=ACCENT_BLUE, scale=0.45)
        sender_car.move_to(LEFT * 5.75 + DOWN * 1.35)
        sender_label = label("SUPPORTER", SIZE_CAPS, ACCENT_BLUE, BOLD)
        sender_label.next_to(sender_car, DOWN, buff=0.14)

        source_feature = feature_tensor()
        source_feature.scale(0.82).move_to(LEFT * 4.25 + DOWN * 1.3)
        source_label = label("FP32 BEV", SIZE_CAPS, RED_ERROR, BOLD)
        source_label.next_to(source_feature, DOWN, buff=0.14)

        book_frame = RoundedRectangle(width=2.15, height=1.55, corner_radius=0.12)
        book_frame.set_fill(PASTEL_AMBER, opacity=0.18)
        book_frame.set_stroke(ACCENT_AMBER, width=1.8, opacity=0.8)
        book = codebook()
        book.move_to(book_frame.get_center() + DOWN * 0.1)
        book_title = label("CODEBOOK", SIZE_CAPS, ACCENT_AMBER, BOLD)
        book_title.move_to(book_frame.get_top() + DOWN * 0.24)
        book_group = VGroup(book_frame, book, book_title)
        book_group.move_to(LEFT * 1.75 + DOWN * 1.3)

        encode_arrow = Arrow(
            [source_feature.get_right()[0] + 0.1, -1.3, 0],
            [book_frame.get_left()[0] - 0.05, -1.3, 0],
            buff=0,
            max_tip_length_to_length_ratio=0.1,
        )
        encode_arrow.set_stroke(ACCENT_AMBER, width=2.2, opacity=0.85)
        encode_arrow.set_fill(ACCENT_AMBER, opacity=0.85)

        packet = index_packet()
        packet.move_to(RIGHT * 0.05 + DOWN * 1.3)
        packet_label = label("LOW-BIT\nINDICES", SIZE_CAPS - 1, GREEN_FIX, BOLD)
        packet_label.next_to(packet, DOWN, buff=0.1)

        self.play(
            FadeIn(sender_car),
            FadeIn(sender_label),
            LaggedStart(
                *(FadeIn(layer, shift=0.08 * RIGHT) for layer in source_feature),
                lag_ratio=0.12,
                run_time=1.0,
            ),
            FadeIn(source_label),
        )
        self.play(
            ShowCreation(encode_arrow),
            FadeIn(book_group, shift=0.1 * RIGHT),
            run_time=0.85,
        )
        self.play(
            TransformFromCopy(source_feature, packet),
            FadeIn(packet_label),
            run_time=1.25,
        )

        # One link only: the packet itself demonstrates that it fits.
        receiver_car = vehicle_icon(color=ACCENT_TEAL, scale=0.45)
        receiver_car.move_to(RIGHT * 5.75 + DOWN * 1.35)
        receiver_label = label("RECEIVER", SIZE_CAPS, ACCENT_TEAL, BOLD)
        receiver_label.next_to(receiver_car, DOWN, buff=0.14)

        reconstructed = feature_tensor(color=ACCENT_TEAL)
        reconstructed.scale(0.82).move_to(RIGHT * 4.25 + DOWN * 1.3)
        reconstructed_label = label("RECONSTRUCTED\nBEV", SIZE_CAPS - 1, ACCENT_TEAL, BOLD)
        reconstructed_label.next_to(reconstructed, DOWN, buff=0.12)

        link = DashedLine(
            [0.72, -1.3, 0],
            [3.3, -1.3, 0],
            dash_length=0.12,
        )
        link.set_stroke(ACCENT_TEAL, width=2.0, opacity=0.55)

        payload_values = VGroup(
            label("100 MB", SIZE_CAPS, RED_ERROR, BOLD),
            label("\u2192", SIZE_CAPS - 1, INK_MID, BOLD),
            label("0.33 MB", SIZE_CAPS, GREEN_FIX, BOLD),
        )
        payload_values.arrange(RIGHT, buff=0.12)
        compression = VGroup(
            label("300x", SIZE_LABEL + 8, GOLD_RICH, BOLD),
            label("SMALLER PAYLOAD", SIZE_CAPS - 1, INK_MID, BOLD),
            payload_values,
        )
        compression.arrange(DOWN, buff=0.08)
        compression.move_to(RIGHT * 2.0 + DOWN * 0.38)

        self.play(
            FadeIn(receiver_car),
            FadeIn(receiver_label),
            ShowCreation(link),
            FadeIn(compression, shift=0.08 * UP),
            run_time=0.95,
        )
 
        # Keep the encoded packet at its source. Only a wrapped copy travels.
        traveling_packet = packet.copy()
        packet_wrap = RoundedRectangle(
            width=traveling_packet.get_width() + 0.2,
            height=traveling_packet.get_height() + 0.2,
            corner_radius=0.08,
        )
        packet_wrap.set_fill(BG_PAPER, opacity=0.92)
        packet_wrap.set_stroke(ACCENT_TEAL, width=1.8, opacity=0.95)
        packet_wrap.move_to(traveling_packet)
        traveling_message = VGroup(packet_wrap, traveling_packet)
        self.add(traveling_message)
        self.play(
            traveling_message.animate.move_to(RIGHT * 4.25 + DOWN * 1.3),
            run_time=2.2,
            rate_func=linear,
        )
        self.play(
            Flash(traveling_message, color=GREEN_FIX, line_length=0.18, num_lines=8),
            run_time=0.4,
        )
        self.play(
            Transform(traveling_message, reconstructed),
            FadeIn(reconstructed_label),
            run_time=1.25,
        )

        deploy_note = label(
            "INT8 model + low-bit messages = fully quantized cooperative perception",
            SIZE_CAPS,
            INK_DARK,
            BOLD,
        )
        deploy_note.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(deploy_note, shift=0.08 * UP), run_time=0.8)
        self.wait(1.5)
        self._close()
