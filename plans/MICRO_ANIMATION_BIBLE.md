# MICRO-ANIMATION BIBLE
## Beyond Self-Driving · Every Single Element Must Bang

> Phần này là BẮT BUỘC đọc trước khi animate bất cứ thứ gì.
> Không có element nào chỉ "FadeIn". Không có text nào chỉ "Write".
> Mọi thứ đều có character riêng.

---

## TRIẾT LÝ CỐT LÕI

Mỗi element khi xuất hiện phải trả lời câu hỏi: **"Nó đến từ đâu?"**

- Text không xuất hiện từ hư không — nó được "viết ra", "chiếu ra", "assembled"
- Box không đột nhiên hiện — nó được "xây", "scan vào", "inject"  
- Arrow không grow — nó "chạy điện", "trace signal", "fire laser"
- Number không chỉ count up — nó "converges", "crystallizes", "locks in"
- Chart không chỉ draw — nó "reveals", "unfolds reality"

Đây không phải exaggeration — đây là storytelling bằng animation.

---

## PHẦN A: TEXT ANIMATIONS

### A1 — Scene Title (đầu mỗi scene)

**KHÔNG dùng: `Write(title)` bình thường**

```python
def scene_title_entrance(title_text: str, color=TEXT_WHITE, 
                          accent_color=CYAN_NEON) -> AnimationGroup:
    """
    Title xuất hiện theo 2 phase:
    Phase 1: Horizontal scan line quét qua từ trái sang phải
    Phase 2: Letters reveal dọc theo scan line (không phải tất cả cùng lúc)
    """
    title = Text(title_text, font_size=SIZE_TITLE, 
                 color=color, font=FONT_PRIMARY)
    title.to_edge(UP, buff=0.3)
    
    # Phase 1: scan line
    scan = Line(
        start=title.get_left() + LEFT*0.2,
        end=title.get_left() + LEFT*0.2,
        stroke_color=accent_color, stroke_width=2.5
    )
    
    # Phase 2: title appears behind scan as it moves right
    # Dùng clip mask: title chỉ visible ở bên trái của scan line
    
    return Succession(
        Create(scan),
        AnimationGroup(
            scan.animate(run_time=0.8, rate_func=smooth)
                .put_start_and_end_on(
                    title.get_left(), title.get_right() + RIGHT*0.2
                ),
            AddTextLetterByLetter(title, run_time=0.7, rate_func=linear),
        ),
        Flash(scan.get_end(), color=accent_color, 
              flash_radius=0.2, num_lines=6, run_time=0.2),
        FadeOut(scan, run_time=0.15)
    )
```

### A2 — Part Name (trên title cards, size 52)

**Hiệu ứng: "Forge" — text được rèn từ nóng chảy**

```python
def forge_text(text_mob, forge_color=GOLD):
    """
    Mỗi letter xuất hiện với màu trắng nóng, rồi nguội về màu đích.
    Letters xuất hiện từng cái, mỗi cái có nhỏ flash phía sau.
    """
    letters = text_mob.submobjects  # Individual letter mobs
    anims = []
    for i, letter in enumerate(letters):
        # Letter bắt đầu ở scale 1.4, màu trắng nóng
        letter_hot = letter.copy().scale(1.4).set_color("#FFFDE7")
        anims.append(
            Succession(
                FadeIn(letter_hot, scale=1.6, run_time=0.04),
                AnimationGroup(
                    letter_hot.animate(run_time=0.15).become(letter),
                    Flash(letter.get_center(), color=forge_color,
                          flash_radius=0.15, num_lines=4, run_time=0.15)
                )
            )
        )
    return LaggedStart(*anims, lag_ratio=0.06)
```

### A3 — Body Explanation Text (size 26, regular paragraphs)

**KHÔNG dùng: `FadeIn(text)` toàn bộ cùng lúc**

```python
def body_text_reveal(text: str, position=ORIGIN, 
                     word_by_word=False) -> AnimationGroup:
    """
    Option 1 (word_by_word=False): Lines reveal từng dòng, từng dòng
    slide in từ LEFT với slight acceleration.
    
    Option 2 (word_by_word=True): từng word một, cho câu key quotes.
    """
    mob = Text(text, font_size=SIZE_BODY, color=TEXT_WHITE,
               font=FONT_PRIMARY, line_spacing=1.4)
    mob.move_to(position)
    
    if not word_by_word:
        lines = mob.submobjects  # Each line as separate mob
        return LaggedStart(*[
            mob_line.animate(run_time=0.35, rate_func=smooth)
                    .shift(RIGHT * 0  # end position
                    ).set_opacity(1)
            # From: mob_line.shift(LEFT * 0.4).set_opacity(0)
            for mob_line in lines
        ], lag_ratio=0.12)
    else:
        # Word by word for emphasis
        words = VGroup(*[
            Text(w, font_size=SIZE_BODY, color=TEXT_WHITE)
            for w in text.split()
        ]).arrange(RIGHT, buff=0.15)
        return LaggedStart(*[
            FadeIn(w, shift=UP*0.08, run_time=0.2)
            for w in words
        ], lag_ratio=0.08)
```

### A4 — Key Terms (gold emphasis words)

Khi một technical term xuất hiện lần đầu (V2X, CooPre, QuantV2X, etc.):

```python
def key_term_reveal(term: str, position=ORIGIN) -> Succession:
    """
    Term xuất hiện với gold color + underline draws + subtle glow ring.
    Dùng cho: first mention của bất kỳ paper name / method name nào.
    """
    term_mob = Text(term, font_size=SIZE_BODY + 2, 
                    color=GOLD, weight=BOLD, font=FONT_PRIMARY)
    term_mob.move_to(position)
    
    underline = Line(
        term_mob.get_left() + DOWN*0.15,
        term_mob.get_left() + DOWN*0.15,  # start: zero length
        stroke_color=GOLD, stroke_width=1.5
    )
    
    glow_ring = Circle(radius=max(term_mob.width, term_mob.height) * 0.6,
                       stroke_color=GOLD, stroke_opacity=0.3, stroke_width=8,
                       fill_opacity=0)
    glow_ring.move_to(term_mob)
    
    return Succession(
        FadeIn(term_mob, scale=0.9, run_time=0.2),
        AnimationGroup(
            underline.animate(run_time=0.3).put_start_and_end_on(
                term_mob.get_left() + DOWN*0.15,
                term_mob.get_right() + DOWN*0.15
            ),
            FadeIn(glow_ring, run_time=0.1),
            glow_ring.animate(run_time=0.4).scale(1.5).set_stroke(opacity=0)
        )
    )
```

### A5 — Statistics / Numbers (1.19M, 94%, 4%, 300×, etc.)

**MỖI số quan trọng phải có counter animation. Không ngoại lệ.**

```python
def stat_reveal(value: float, label: str, 
                color=GOLD, font_size=SIZE_HERO,
                milestone_effect=True) -> VGroup:
    """
    Counter animation với milestone burst.
    value: final number
    milestone_effect: nếu True, khi counter đạt số đích có particle burst
    """
    counter = DecimalNumber(
        0, num_decimal_places=0,
        color=color, font_size=font_size
    )
    
    label_mob = Text(label, font_size=SIZE_LABEL, 
                     color=TEXT_DIM, font=FONT_PRIMARY)
    
    group = VGroup(counter, label_mob).arrange(DOWN, buff=0.2)
    
    def counter_update(mob, alpha):
        mob.set_value(int(alpha * value))
        # Color shifts: dim → target color as counter rises
        mob.set_color(interpolate_color(TEXT_GHOST, color, alpha**0.5))
    
    anim = AnimationGroup(
        UpdateFromAlphaFunc(counter, counter_update, run_time=1.8,
                           rate_func=smooth),
        FadeIn(label_mob, shift=UP*0.1, run_time=0.5)
    )
    
    if milestone_effect:
        burst = AnimationGroup(
            Flash(counter, color=color, flash_radius=0.8, 
                  num_lines=12, run_time=0.4),
            counter.animate(run_time=0.15).scale(1.2),
            counter.animate(run_time=0.15).scale(1/1.2),
        )
        return Succession(anim, burst)
    
    return anim
```

### A6 — Inline Bullets / Lists

**KHÔNG reveal tất cả cùng lúc. Mỗi bullet reveal khi cần.**

```python
def bullet_reveal(items: list[str], 
                  accent_color=CYAN_NEON,
                  stagger=0.15) -> LaggedStart:
    """
    Mỗi bullet:
    1. Bullet dot flashes in (tiny circle)
    2. Text writes in từ LEFT (không phải FadeIn)
    """
    mobs = VGroup()
    for text in items:
        dot = Dot(radius=0.06, color=accent_color)
        line = Text(text, font_size=SIZE_BODY, 
                    color=TEXT_WHITE, font=FONT_PRIMARY)
        row = VGroup(dot, line).arrange(RIGHT, buff=0.25)
        mobs.add(row)
    mobs.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    
    anims = []
    for row in mobs:
        dot, line = row[0], row[1]
        anims.append(
            Succession(
                GrowFromCenter(dot, run_time=0.12),
                Flash(dot, color=accent_color, flash_radius=0.12, 
                      num_lines=4, run_time=0.12),
                AddTextLetterByLetter(line, run_time=0.3),
            )
        )
    return LaggedStart(*anims, lag_ratio=stagger)
```

### A7 — Quote Reveals (italic gold, key takeaways)

**Quotes là khoảnh khắc sacred. Phải có weight.**

```python
def quote_reveal(quote_text: str, author: str = "") -> Succession:
    """
    Phase 1: Hai horizontal lines appear (top và bottom) — "framing" the quote
    Phase 2: Quote text appears word by word, slow
    Phase 3: Author appears, dimmer
    Phase 4: Brief hold, then lines pulse once
    """
    quote = Text(f'"{quote_text}"', 
                 font_size=SIZE_BODY + 4, slant=ITALIC,
                 color=GOLD, font=FONT_PRIMARY,
                 line_spacing=1.5)
    quote.move_to(ORIGIN)
    
    top_line = Line(
        quote.get_left(), quote.get_left(),  # Zero width initially
        stroke_color=GOLD, stroke_width=1.2, stroke_opacity=0.5
    )
    bot_line = top_line.copy()
    top_line.shift(UP * (quote.height/2 + 0.2))
    bot_line.shift(DOWN * (quote.height/2 + 0.2))
    
    author_mob = Text(f"— {author}", font_size=SIZE_LABEL,
                      color=TEXT_DIM, slant=ITALIC)
    author_mob.next_to(quote, DOWN, buff=0.3).to_edge(RIGHT, buff=1.0)
    
    words = quote.text.split()
    
    return Succession(
        # Frame lines draw
        AnimationGroup(
            top_line.animate(run_time=0.5).put_start_and_end_on(
                quote.get_left() + UP*(quote.height/2+0.2),
                quote.get_right() + UP*(quote.height/2+0.2)
            ),
            bot_line.animate(run_time=0.5).put_start_and_end_on(
                quote.get_left() + DOWN*(quote.height/2+0.2),
                quote.get_right() + DOWN*(quote.height/2+0.2)
            ),
        ),
        # Quote word by word (slower — let it breathe)
        AddTextLetterByLetter(quote, run_time=len(words)*0.12),
        # Author
        FadeIn(author_mob, shift=LEFT*0.1, run_time=0.4) if author else Wait(0),
        # Pulse the frame lines
        AnimationGroup(
            top_line.animate(run_time=0.3).set_stroke(opacity=1.0),
            bot_line.animate(run_time=0.3).set_stroke(opacity=1.0),
        ),
        AnimationGroup(
            top_line.animate(run_time=0.3).set_stroke(opacity=0.4),
            bot_line.animate(run_time=0.3).set_stroke(opacity=0.4),
        ),
    )
```

### A8 — Citation / Footnote (tiny, bottom of screen)

```python
def citation_reveal(text: str) -> FadeIn:
    """
    Footnotes không cần drama — subtle FadeIn từ bottom edge.
    """
    mob = Text(text, font_size=SIZE_MICRO, color=TEXT_GHOST,
               font=FONT_PRIMARY)
    mob.to_corner(DL, buff=0.2)
    mob.shift(DOWN * 0.3)  # Start slightly below safe zone
    return mob.animate(run_time=0.5, rate_func=smooth).shift(UP * 0.3)
```

---

## PHẦN B: BOX / BLOCK ANIMATIONS

### B1 — Pipeline Block (standard appearance)

**KHÔNG dùng: `FadeIn(block)`**

```python
def pipeline_block_entrance(block: VGroup, 
                             direction="from_left",
                             accent_color=CYAN_NEON) -> Succession:
    """
    Phase 1: Border "assembles" — 4 corners xuất hiện trước, 
             rồi lines draw inward để meet nhau
    Phase 2: Fill "floods in" như liquid
    Phase 3: Label text appears (scan line style)
    """
    rect, label = block[0], block[1]
    
    # Phase 1: Corner dots → border trace
    corners = [rect.get_corner(d) for d in [UL, UR, DR, DL]]
    corner_dots = VGroup(*[
        Dot(radius=0.05, color=accent_color).move_to(c)
        for c in corners
    ])
    
    return Succession(
        # Corners flash in simultaneously
        LaggedStart(*[
            GrowFromCenter(d, run_time=0.08) for d in corner_dots
        ], lag_ratio=0.1),
        # Border draws connecting corners
        AnimationGroup(
            Create(rect, run_time=0.4, rate_func=smooth),
            FadeOut(corner_dots, run_time=0.2),
        ),
        # Fill floods from bottom
        rect.animate(run_time=0.25).set_fill(
            rect.fill_color, opacity=1.0
        ),
        # Label scan-reveal
        AddTextLetterByLetter(label, run_time=0.3),
    )
```

### B2 — Highlight Box / Info Panel (big panels with content)

```python
def info_panel_entrance(panel: VGroup, 
                         scan_color=CYAN_NEON) -> Succession:
    """
    Panel như một hologram được "projected" vào không gian:
    Phase 1: Horizontal scan line sweeps top → bottom
    Phase 2: Content appears behind scan as it passes
    Phase 3: Final shimmer (one more scan, fast)
    """
    rect, *contents = panel
    
    scan_line = Line(
        rect.get_left() + UP * rect.height/2,
        rect.get_right() + UP * rect.height/2,
        stroke_color=scan_color, stroke_width=2.0, stroke_opacity=0.8
    )
    
    return Succession(
        # Panel border appears
        Create(rect, run_time=0.5),
        # Scan line sweeps down, revealing content
        AnimationGroup(
            scan_line.animate(run_time=0.7, rate_func=linear)
                     .shift(DOWN * rect.height),
            LaggedStart(*[
                FadeIn(c, shift=DOWN*0.05, run_time=0.2)
                for c in contents
            ], lag_ratio=0.1),
        ),
        # Shimmer: fast scan up and out
        scan_line.animate(run_time=0.25, rate_func=rush_into)
                 .shift(UP * rect.height * 2)
                 .set_stroke(opacity=0),
    )
```

### B3 — Result Box (khi reveal số liệu kết quả)

```python
def result_box_entrance(box: VGroup, 
                         good_result=True) -> Succession:
    """
    Kết quả tốt (good_result=True): box "stamps" in từ trên xuống
    với green flash + check mark momentarily visible
    
    Kết quả xấu: box shakes và turns red briefly
    """
    rect, label = box[0], box[1]
    
    if good_result:
        check = Text("✓", font_size=40, color=GREEN_SIGNAL)
        check.move_to(rect)
        
        return Succession(
            # Stamp animation: drop from above với slight bounce
            FadeIn(rect, shift=DOWN*0.4, scale=1.1, run_time=0.25),
            rect.animate(run_time=0.1).scale(1/1.1),
            # Check mark flash
            AnimationGroup(
                FadeIn(check, scale=1.5, run_time=0.15),
                FadeOut(check, scale=2.0, run_time=0.25),
            ),
            # Label settles in
            FadeIn(label, run_time=0.2),
            # Glow ring
            Flash(rect.get_center(), color=GREEN_SIGNAL,
                  flash_radius=max(rect.width, rect.height)*0.6,
                  num_lines=8, run_time=0.35),
        )
    else:
        return Succession(
            FadeIn(box, run_time=0.2),
            box.animate(run_time=0.06).shift(RIGHT*0.1),
            box.animate(run_time=0.06).shift(LEFT*0.2),
            box.animate(run_time=0.06).shift(RIGHT*0.1),
        )
```

### B4 — Comparison Boxes (Before vs After)

```python
def before_after_reveal(before_box: VGroup, after_box: VGroup,
                         divider_color=TEXT_DIM) -> Succession:
    """
    Before/After pattern dùng trong nhiều scene:
    1. Before xuất hiện trước (LEFT side)
    2. Vertical divider draws từ top → bottom
    3. After xuất hiện (RIGHT side) với glow
    """
    divider = Line(UP*3, UP*3, stroke_color=divider_color, stroke_width=1.0)
    divider.move_to(ORIGIN).shift(UP*3)  # Start at top
    
    before_label = Text("BEFORE", font_size=SIZE_MICRO, color=TEXT_DIM)
    before_label.next_to(before_box, UP, buff=0.15)
    after_label = Text("AFTER", font_size=SIZE_MICRO, color=GREEN_SIGNAL)
    after_label.next_to(after_box, UP, buff=0.15)
    
    return Succession(
        # Before appears, slightly dim
        FadeIn(VGroup(before_box, before_label), 
               shift=RIGHT*0.15, run_time=0.4),
        before_box.animate(run_time=0.2).set_opacity(0.6),
        # Divider drops
        divider.animate(run_time=0.4, rate_func=rush_into)
               .put_start_and_end_on(UP*3.5, DOWN*3.5),
        # After reveals with enthusiasm
        FadeIn(VGroup(after_box, after_label), 
               shift=LEFT*0.2, run_time=0.3),
        Flash(after_box.get_center(), color=GREEN_SIGNAL,
              flash_radius=0.8, num_lines=10, run_time=0.4),
        # Before fades more, after brightens
        AnimationGroup(
            before_box.animate(run_time=0.3).set_opacity(0.4),
            after_box.animate(run_time=0.3).set_stroke(GREEN_SIGNAL, width=2.5),
        )
    )
```

### B5 — Neural Network Block (for model diagrams)

```python
def neural_block_entrance(block: VGroup, 
                            neural_color=PURPLE_MODEL) -> Succession:
    """
    Neural net blocks shimmer với "thinking" effect:
    Tiny dots inside block animate briefly — suggests computation.
    """
    rect, label = block[0], block[1]
    
    # Internal "neurons" — tiny dots inside block
    n_dots = 12
    internal_dots = VGroup(*[
        Dot(
            radius=0.035,
            color=neural_color,
            fill_opacity=np.random.uniform(0.2, 0.8)
        ).move_to([
            rect.get_center()[0] + np.random.uniform(-rect.width*0.35, rect.width*0.35),
            rect.get_center()[1] + np.random.uniform(-rect.height*0.35, rect.height*0.35),
            0
        ])
        for _ in range(n_dots)
    ])
    
    def shimmer_update(group, alpha):
        for dot in group:
            phase = np.random.random()
            dot.set_fill(opacity=0.2 + 0.6 * abs(np.sin(alpha * np.pi * 3 + phase * 2)))
    
    return Succession(
        Create(rect, run_time=0.4),
        AnimationGroup(
            FadeIn(internal_dots, run_time=0.2),
            UpdateFromAlphaFunc(internal_dots, shimmer_update, run_time=0.6),
        ),
        AnimationGroup(
            FadeOut(internal_dots, run_time=0.25),
            FadeIn(label, run_time=0.25),
        )
    )
```

---

## PHẦN C: ARROW / CONNECTION ANIMATIONS

### C1 — Standard Pipeline Arrow

**KHÔNG dùng: `Create(arrow)` thường**

```python
def pipeline_arrow_entrance(arrow: Arrow, 
                              style="electric") -> Animation:
    """
    style="electric": Lightning bolt trace (nhanh, nhọn)
    style="data":     Dots stream along path before arrow solidifies
    style="beam":     Laser beam fires từ start → end
    """
    if style == "electric":
        # Arrow draws nhanh như lightning
        return Succession(
            Create(arrow, run_time=0.18, rate_func=rush_into),
            Flash(arrow.get_end(), 
                  color=arrow.get_color(),
                  flash_radius=0.15, num_lines=5, run_time=0.12)
        )
    
    elif style == "data":
        # Dots travel first, arrow materializes after
        path_line = arrow.copy().set_stroke(
            arrow.get_color(), width=0.8, opacity=0.3
        )
        dots = VGroup(*[
            Dot(radius=0.04, color=arrow.get_color(),
                fill_opacity=0.9).move_to(arrow.get_start())
            for _ in range(5)
        ])
        return Succession(
            Create(path_line, run_time=0.15),
            LaggedStart(*[
                MoveAlongPath(d, arrow.copy().set_opacity(0),
                             run_time=0.4)
                for d in dots
            ], lag_ratio=0.12),
            AnimationGroup(
                Create(arrow, run_time=0.2),
                FadeOut(path_line, run_time=0.15),
                FadeOut(dots, run_time=0.1),
            )
        )
    
    elif style == "beam":
        # Laser beam: fast, bright, leave brief afterglow
        glow_arrow = arrow.copy().set_stroke(
            width=arrow.get_stroke_width() * 4,
            opacity=0.15
        )
        return Succession(
            Create(arrow, run_time=0.12, rate_func=linear),
            AnimationGroup(
                FadeIn(glow_arrow, run_time=0.05),
                glow_arrow.animate(run_time=0.25).set_stroke(opacity=0)
            )
        )
```

### C2 — V2X Communication Link (Vehicle-to-Vehicle)

```python
def v2x_link_pulse(node_a: Mobject, node_b: Mobject,
                    link_color=COMM_LINK,
                    bidirectional=True) -> AnimationGroup:
    """
    Communication link giữa 2 agents:
    - Persistent thin line (stays visible)
    - Periodic data packets travel along it
    - Nếu bidirectional: packets go BOTH ways simultaneously
    """
    link_line = DashedLine(
        node_a.get_center(), node_b.get_center(),
        color=link_color, stroke_width=1.2, stroke_opacity=0.4,
        dash_length=0.15
    )
    
    # Packet: small hexagon (data packet shape)
    def make_packet(color=link_color):
        return RegularPolygon(n=6, radius=0.06, 
                             color=color, fill_opacity=0.9)
    
    pkt_a_to_b = make_packet()
    pkt_b_to_a = make_packet()
    pkt_a_to_b.move_to(node_a.get_center())
    pkt_b_to_a.move_to(node_b.get_center())
    
    path_ab = Line(node_a.get_center(), node_b.get_center())
    path_ba = Line(node_b.get_center(), node_a.get_center())
    
    packet_flow = AnimationGroup(
        Succession(
            MoveAlongPath(pkt_a_to_b, path_ab, run_time=0.6, rate_func=linear),
            Flash(node_b.get_center(), color=link_color, 
                  flash_radius=0.15, run_time=0.1),
            FadeOut(pkt_a_to_b, run_time=0.05),
        ),
        Succession(
            Wait(0.3),  # Offset
            MoveAlongPath(pkt_b_to_a, path_ba, run_time=0.6, rate_func=linear),
            Flash(node_a.get_center(), color=link_color,
                  flash_radius=0.15, run_time=0.1),
            FadeOut(pkt_b_to_a, run_time=0.05),
        ) if bidirectional else Wait(0)
    )
    
    return Succession(
        Create(link_line, run_time=0.35),
        packet_flow
    )
```

### C3 — Error Propagation Arrow (cascade failure)

```python
def error_cascade_arrow(arrows: list[Arrow]) -> LaggedStart:
    """
    Error propagates through pipeline arrows:
    Each arrow flashes RED, shakes, then settles (indicating bad signal)
    """
    anims = []
    for arrow in arrows:
        original_color = arrow.get_color()
        anims.append(
            Succession(
                arrow.animate(run_time=0.15).set_color(RED_ALERT).set_stroke(width=4),
                # Vibrate
                arrow.animate(run_time=0.06).shift(UP*0.05),
                arrow.animate(run_time=0.06).shift(DOWN*0.1),
                arrow.animate(run_time=0.06).shift(UP*0.05),
                # Settle with error color
                arrow.animate(run_time=0.2)
                     .set_color(interpolate_color(RED_ALERT, original_color, 0.3))
                     .set_stroke(width=2),
            )
        )
    return LaggedStart(*anims, lag_ratio=0.25)
```

---

## PHẦN D: CHART / GRAPH ANIMATIONS

### D1 — Axes Entrance

**KHÔNG chỉ `Create(axes)` — axes phải DEPLOY**

```python
def axes_deploy(axes: Axes, 
                 label_x: str, label_y: str) -> Succession:
    """
    Axes deploy như radar scanner khởi động:
    1. Origin point flashes
    2. X-axis shoots right
    3. Y-axis shoots up  
    4. Ticks appear LaggedStart
    5. Labels appear
    """
    origin_flash = Flash(axes.get_origin(),
                         color=CYAN_NEON, flash_radius=0.2,
                         num_lines=8, run_time=0.2)
    
    x_line = axes.x_axis
    y_line = axes.y_axis
    x_ticks = axes.get_x_axis().ticks if hasattr(axes.get_x_axis(), 'ticks') else VGroup()
    y_ticks = axes.get_y_axis().ticks if hasattr(axes.get_y_axis(), 'ticks') else VGroup()
    
    x_label_mob = Text(label_x, font_size=SIZE_LABEL, color=TEXT_DIM)
    y_label_mob = Text(label_y, font_size=SIZE_LABEL, color=TEXT_DIM)
    x_label_mob.next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
    y_label_mob.next_to(axes.y_axis.get_end(), UP, buff=0.15)
    
    return Succession(
        origin_flash,
        AnimationGroup(
            Create(x_line, run_time=0.35, rate_func=rush_into),
            Succession(
                Wait(0.1),
                Create(y_line, run_time=0.35, rate_func=rush_into),
            )
        ),
        LaggedStart(
            *[GrowFromCenter(t, run_time=0.08) for t in x_ticks],
            *[GrowFromCenter(t, run_time=0.08) for t in y_ticks],
            lag_ratio=0.05
        ),
        AnimationGroup(
            FadeIn(x_label_mob, shift=RIGHT*0.1, run_time=0.25),
            FadeIn(y_label_mob, shift=UP*0.1, run_time=0.25),
        )
    )
```

### D2 — Bar Chart Bars (growing upward)

```python
def bar_grow(bar: Rectangle, target_height: float,
              bar_color: str, label_value: str) -> Succession:
    """
    Bar grows từ bottom với:
    - Particle trail phía trên bar đang grow
    - Counter animate đồng bộ với bar height
    - Khi bar đạt đỉnh: Flash + value locks in
    """
    bar.stretch_to_fit_height(0.01)
    bar.to_edge(DOWN, buff=0.5)
    
    counter = Text("0", font_size=SIZE_LABEL, color=bar_color)
    counter.add_updater(lambda m: m.next_to(bar, UP, buff=0.1))
    
    # Particle emitter at bar top
    def make_particle():
        return Dot(
            radius=0.025,
            color=bar_color,
            fill_opacity=0.7
        ).move_to(bar.get_top())
    
    particles = VGroup(*[make_particle() for _ in range(6)])
    
    grow_tracker = ValueTracker(0.01)
    
    def bar_updater(b):
        new_h = grow_tracker.get_value() * target_height
        b.stretch_to_fit_height(max(new_h, 0.01))
        b.to_edge(DOWN, buff=0.5)
    
    def counter_updater(m):
        val = int(grow_tracker.get_value() * float(label_value.replace(',', '').replace('K', '000').replace('M', '000000')))
        m.become(Text(f"{val:,}", font_size=SIZE_LABEL, color=bar_color))
        m.next_to(bar, UP, buff=0.1)
    
    bar.add_updater(bar_updater)
    counter.add_updater(counter_updater)
    
    return Succession(
        AnimationGroup(
            grow_tracker.animate(run_time=1.2, rate_func=smooth).set_value(1.0),
            LaggedStart(*[
                Succession(
                    Wait(np.random.random() * 0.8),
                    particles[i].animate(run_time=0.4, rate_func=rush_from)
                               .shift(UP * np.random.uniform(0.2, 0.6))
                               .set_fill(opacity=0),
                )
                for i in range(6)
            ], lag_ratio=0.1)
        ),
        # Lock-in flash
        Flash(bar.get_top(), color=bar_color, 
              flash_radius=0.3, num_lines=6, run_time=0.25),
        # Remove updaters, add final static label
        RemoveUpdater(bar, bar_updater),
        RemoveUpdater(counter, counter_updater),
    )
```

### D3 — Line/Curve Plot

```python
def curve_trace(axes: Axes, func, color, 
                 x_range=None, glow=True) -> Succession:
    """
    Curve draws với glowing "head" tracing along path.
    Sau khi curve hoàn thành, glow fades và để lại clean curve.
    Nếu glow=True: thick glow layer under thin clean curve.
    """
    x_start, x_end = x_range or [axes.x_range[0], axes.x_range[1]]
    
    # Main curve
    main_curve = axes.plot(func, x_range=[x_start, x_end],
                           color=color, stroke_width=2.5)
    
    if glow:
        # Glow layer: same curve, wider, more transparent
        glow_curve = axes.plot(func, x_range=[x_start, x_end],
                               color=color, stroke_width=8,
                               stroke_opacity=0.2)
    
    # Head: bright dot traveling along curve
    head = Dot(radius=0.08, color=WHITE, fill_opacity=1.0)
    head_trail = TracedPath(head.get_center, stroke_color=color,
                            stroke_width=3, dissipating_time=0.3)
    head.move_to(axes.input_to_graph_point(x_start, main_curve))
    
    x_tracker = ValueTracker(x_start)
    
    def head_updater(h):
        x = x_tracker.get_value()
        try:
            h.move_to(axes.input_to_graph_point(x, main_curve))
        except:
            pass
    
    head.add_updater(head_updater)
    
    return Succession(
        AnimationGroup(
            FadeIn(head, run_time=0.1),
            FadeIn(head_trail, run_time=0.1),
        ),
        AnimationGroup(
            x_tracker.animate(run_time=1.5, rate_func=smooth)
                     .set_value(x_end),
            Create(main_curve, run_time=1.5, rate_func=smooth),
        ),
        AnimationGroup(
            FadeOut(head, run_time=0.2),
            FadeOut(head_trail, run_time=0.2),
            FadeIn(glow_curve, run_time=0.2) if glow else Wait(0),
        ),
        RemoveUpdater(head, head_updater),
    )
```

### D4 — Scatter Points / Data Points

```python
def scatter_reveal(points: VGroup, 
                    reveal_style="rain") -> Animation:
    """
    reveal_style="rain": points fall from above (như mưa data)
    reveal_style="burst": all points burst from center simultaneously
    reveal_style="scan": points appear left→right theo cột
    """
    if reveal_style == "rain":
        anims = []
        for p in points:
            start_pos = p.get_center() + UP * np.random.uniform(1.5, 4.0)
            p.move_to(start_pos)
            anims.append(
                p.animate(
                    run_time=np.random.uniform(0.3, 0.7),
                    rate_func=rush_into
                ).move_to(start_pos - UP * (start_pos[1] - p.get_center()[1]))
            )
        return LaggedStart(*anims, lag_ratio=0.04)
    
    elif reveal_style == "burst":
        center = points.get_center()
        original_positions = [p.get_center().copy() for p in points]
        for p in points:
            p.move_to(center)
        return AnimationGroup(*[
            p.animate(run_time=0.5, rate_func=rush_from)
             .move_to(original_positions[i])
            for i, p in enumerate(points)
        ])
    
    elif reveal_style == "scan":
        points_sorted = sorted(points, key=lambda p: p.get_center()[0])
        return LaggedStart(*[
            GrowFromCenter(p, run_time=0.1)
            for p in points_sorted
        ], lag_ratio=0.06)
```

### D5 — Power-Law / Distribution Curve (đặc biệt cho Long-tail và MetaUrban)

```python
def power_law_reveal(axes, x_range, color=P5_PHYSICAL) -> Succession:
    """
    Power-law có ý nghĩa đặc biệt — không chỉ trace curve.
    1. Curve traces từ LEFT (high values)
    2. Khi curve bắt đầu dốc xuống: vertical line drops → "the cliff"
    3. TAIL region: highlight với different color, pulse
    4. Label "Long tail" appears với arrow pointing to tail
    """
    func = lambda x: min(2.0, 2.0 * max(x, 0.1) ** (-1.3))
    
    main_curve = axes.plot(func, x_range=x_range, 
                           color=color, stroke_width=3)
    
    # "Cliff" visual: area under left side (common scenarios)
    common_area = axes.get_area(
        main_curve, x_range=[x_range[0], x_range[0] + (x_range[1]-x_range[0])*0.15],
        color=color, opacity=0.25
    )
    
    # Tail area: highlight different
    tail_area = axes.get_area(
        main_curve, x_range=[x_range[0] + (x_range[1]-x_range[0])*0.3, x_range[1]],
        color=RED_ALERT, opacity=0.2
    )
    
    tail_label = Text("Long Tail\n(edge cases)", font_size=SIZE_LABEL,
                      color=RED_ALERT)
    tail_label.next_to(axes.input_to_graph_point(x_range[1]*0.7, main_curve),
                       UP + RIGHT, buff=0.2)
    tail_arrow = Arrow(
        tail_label.get_bottom(),
        axes.input_to_graph_point(x_range[1]*0.8, main_curve),
        color=RED_ALERT, stroke_width=1.5, tip_length=0.15
    )
    
    return Succession(
        curve_trace(axes, func, color, x_range, glow=True),
        FadeIn(common_area, run_time=0.4),
        FadeIn(tail_area, run_time=0.5),
        AnimationGroup(
            FadeIn(tail_label, shift=DOWN*0.1, run_time=0.3),
            Create(tail_arrow, run_time=0.3),
        ),
        # Tail pulses — "this is where accidents happen"
        AnimationGroup(
            tail_area.animate(run_time=0.4).set_fill(opacity=0.45),
            tail_area.animate(run_time=0.4).set_fill(opacity=0.2),
        )
    )
```

---

## PHẦN E: ICON / SYMBOL ANIMATIONS

### E1 — Car Icon (agent representation)

```python
def car_icon_entrance(car: VGroup, 
                       direction=RIGHT) -> Succession:
    """
    Car drives in từ edge của screen (không xuất hiện ở đó sẵn).
    Tires "rolling" effect (rotation của wheel circles).
    """
    body, *wheels = car
    
    # Start off-screen
    car.shift(-direction * 8)
    
    def wheels_spin(group, alpha):
        for wheel in group:
            wheel.rotate(alpha * TAU * 2)
    
    return Succession(
        AnimationGroup(
            car.animate(run_time=0.8, rate_func=smooth)
               .shift(direction * 8),  # Drive to position
            UpdateFromAlphaFunc(
                VGroup(*wheels),
                wheels_spin,
                run_time=0.8
            )
        ),
        # Brake effect: brief squish
        car.animate(run_time=0.08).stretch(1.1, 0).stretch(0.95, 1),
        car.animate(run_time=0.08).stretch(1/1.1, 0).stretch(1/0.95, 1),
    )
```

### E2 — Building / Obstacle (occlusion scene)

```python
def building_drop(building: VGroup) -> Succession:
    """
    Building drops từ sky như a heavy block.
    Impact: slight camera shake effect + dust particles.
    """
    original_pos = building.get_center()
    building.shift(UP * 6)  # Start high above
    
    dust_particles = VGroup(*[
        Dot(radius=0.04, color=TEXT_DIM, fill_opacity=0.6)
        .move_to(original_pos + np.array([
            np.random.uniform(-building.width*0.6, building.width*0.6),
            -building.height/2 - 0.1,
            0
        ]))
        for _ in range(10)
    ])
    
    return Succession(
        # Drop with gravity acceleration
        building.animate(run_time=0.45, rate_func=rush_into)
                .move_to(original_pos),
        # Impact: squish
        building.animate(run_time=0.06).stretch(1.15, 0).stretch(0.9, 1),
        building.animate(run_time=0.06).stretch(1/1.15, 0).stretch(1/0.9, 1),
        # Dust
        AnimationGroup(
            FadeIn(dust_particles, run_time=0.1),
            LaggedStart(*[
                p.animate(run_time=0.4, rate_func=rush_from)
                 .shift(np.array([
                     np.random.uniform(-0.5, 0.5),
                     np.random.uniform(0.1, 0.5),
                     0
                 ])).set_fill(opacity=0)
                for p in dust_particles
            ], lag_ratio=0.05)
        )
    )
```

### E3 — Checkmark / X-mark (result indicators)

```python
def checkmark_stamp(position, color=GREEN_SIGNAL) -> Succession:
    check = Text("✓", font_size=36, color=color).move_to(position)
    ring = Circle(radius=0.3, color=color, 
                  stroke_width=2, fill_opacity=0)
    ring.move_to(position)
    
    return Succession(
        GrowFromCenter(check, run_time=0.2),
        AnimationGroup(
            Flash(position, color=color, flash_radius=0.4, 
                  num_lines=8, run_time=0.3),
            ring.animate(run_time=0.4).scale(2).set_stroke(opacity=0),
        )
    )

def xmark_appear(position, color=RED_ALERT) -> Succession:
    xmark = Text("✗", font_size=36, color=color).move_to(position)
    
    return Succession(
        FadeIn(xmark, scale=1.5, run_time=0.15),
        xmark.animate(run_time=0.1).scale(1/1.5),
        # Shake
        xmark.animate(run_time=0.05).shift(RIGHT*0.08),
        xmark.animate(run_time=0.05).shift(LEFT*0.16),
        xmark.animate(run_time=0.05).shift(RIGHT*0.08),
    )
```

### E4 — Hexagon Icons (FM icons floating above car)

```python
def fm_icon_cluster(labels: list[str], center: np.ndarray,
                     color=P1_FOUNDATION) -> tuple[VGroup, Succession]:
    """
    Floating hexagon cluster cho Foundation Model icons.
    Returns (mob_group, entrance_animation)
    """
    hexagons = VGroup()
    positions = [
        center + np.array([-0.7, 0.7, 0]),
        center + np.array([0, 0.9, 0]),
        center + np.array([0.7, 0.7, 0]),
    ]
    
    for i, (label, pos) in enumerate(zip(labels, positions)):
        hex_bg = RegularPolygon(n=6, radius=0.25, 
                               color=color, fill_opacity=0.3,
                               stroke_width=1.5).move_to(pos)
        hex_label = Text(label, font_size=10, color=color).move_to(pos)
        hexagons.add(VGroup(hex_bg, hex_label))
    
    # Connecting wires
    wires = VGroup()
    for i, hex_a in enumerate(hexagons):
        for hex_b in hexagons[i+1:]:
            wire = DashedLine(
                hex_a.get_center(), hex_b.get_center(),
                stroke_color=color, stroke_width=0.6,
                stroke_opacity=0.4, dash_length=0.08
            )
            wires.add(wire)
    
    full_group = VGroup(hexagons, wires)
    
    entrance = LaggedStart(
        *[
            Succession(
                GrowFromCenter(h[0], run_time=0.2),
                FadeIn(h[1], run_time=0.15),
            )
            for h in hexagons
        ],
        LaggedStart(*[
            Create(w, run_time=0.15) for w in wires
        ], lag_ratio=0.1),
        lag_ratio=0.2
    )
    
    # Floating animation: oscillate gently (use always_redraw)
    def float_update(group, dt):
        t = group.float_time if hasattr(group, 'float_time') else 0
        group.float_time = t + dt
        group.shift(UP * np.sin(t * 1.5) * 0.003)
    
    full_group.add_updater(float_update)
    
    return full_group, entrance
```

---

## PHẦN F: BACKGROUND AMBIENT ANIMATIONS

**Mỗi scene có background "thở" — không bao giờ static hoàn toàn.**

### F1 — Default Body Scene Background

```python
def setup_ambient_background(scene: Scene) -> None:
    """
    Gọi ở đầu mọi body scene (không phải title cards).
    Tạo subtle particle drift — không distract nhưng scene "sống".
    """
    n_particles = 25
    particles = VGroup(*[
        Dot(
            radius=np.random.uniform(0.015, 0.04),
            color=CYAN_NEON,
            fill_opacity=np.random.uniform(0.03, 0.10)
        ).move_to([
            np.random.uniform(-7, 7),
            np.random.uniform(-4, 4),
            0
        ])
        for _ in range(n_particles)
    ])
    
    speeds = [np.array([
        np.random.uniform(-0.008, 0.008),
        np.random.uniform(-0.003, 0.003),
        0
    ]) for _ in range(n_particles)]
    
    def drift_updater(group, dt):
        for i, p in enumerate(group):
            p.shift(speeds[i])
            # Wrap around screen edges
            if p.get_center()[0] > 7.5:
                p.shift(LEFT * 15)
            elif p.get_center()[0] < -7.5:
                p.shift(RIGHT * 15)
            if p.get_center()[1] > 4.5:
                p.shift(DOWN * 9)
            elif p.get_center()[1] < -4.5:
                p.shift(UP * 9)
    
    particles.add_updater(drift_updater)
    scene.add(particles)
    return particles  # Return để có thể FadeOut cuối scene
```

### F2 — Part-Specific Ambient (background theme per part)

```python
# Part 1: Neural network floating in background
def p1_ambient(scene):
    """Faint neural net graph drifting — fits Foundation Models theme"""
    n_nodes = 12
    nodes = VGroup(*[
        Dot(radius=0.04, color=P1_FOUNDATION, fill_opacity=0.06)
        .move_to([np.random.uniform(-6, 6), np.random.uniform(-3, 3), 0])
        for _ in range(n_nodes)
    ])
    edges = VGroup()
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if np.random.random() < 0.3:
                line = Line(nodes[i].get_center(), nodes[j].get_center(),
                           stroke_color=P1_FOUNDATION, 
                           stroke_width=0.4, stroke_opacity=0.04)
                edges.add(line)
    
    def pulse_updater(group, dt):
        for node in group:
            node.set_fill(opacity=node.fill_opacity * 0.995 + 
                         np.random.uniform(-0.002, 0.002))
    
    nodes.add_updater(pulse_updater)
    scene.add_to_back(VGroup(edges, nodes))

# Part 2: Faint radar rings drifting across background
def p2_ambient(scene):
    """Background radar rings — reinforces V2X theme"""
    rings = VGroup()
    for _ in range(6):
        r = Circle(
            radius=np.random.uniform(0.5, 2.5),
            stroke_color=CYAN_NEON,
            stroke_width=0.5,
            stroke_opacity=np.random.uniform(0.02, 0.06)
        ).move_to([np.random.uniform(-6, 6), np.random.uniform(-3, 3), 0])
        rings.add(r)
    
    def expand_updater(group, dt):
        for ring in group:
            ring.scale(1 + dt * 0.05)  # Slowly expand
            # Reset when too big
            if ring.radius > 5:
                ring.scale(0.1)
                ring.set_stroke(opacity=0.06)
            else:
                ring.set_stroke(opacity=max(0, ring.get_stroke_opacity() - dt * 0.005))
    
    rings.add_updater(expand_updater)
    scene.add_to_back(rings)

# Part 4: Falling bits (quantization theme)
def p4_ambient(scene):
    """Falling binary digits — efficiency/quantization theme"""
    digits = VGroup(*[
        Text(
            np.random.choice(["0", "1"]),
            font_size=10, color=P4_EFFICIENT,
            fill_opacity=np.random.uniform(0.05, 0.15)
        ).move_to([
            np.random.uniform(-7, 7),
            np.random.uniform(-4, 5),
            0
        ])
        for _ in range(40)
    ])
    
    fall_speeds = [np.random.uniform(0.01, 0.04) for _ in range(40)]
    
    def fall_updater(group, dt):
        for i, d in enumerate(group):
            d.shift(DOWN * fall_speeds[i])
            if d.get_center()[1] < -4.5:
                d.move_to([
                    np.random.uniform(-7, 7),
                    4.5,
                    0
                ])
                d.become(Text(
                    np.random.choice(["0", "1"]),
                    font_size=10, color=P4_EFFICIENT,
                    fill_opacity=np.random.uniform(0.05, 0.15)
                ).move_to(d.get_center()))
    
    digits.add_updater(fall_updater)
    scene.add_to_back(digits)

# Part 5: City grid faint in background
def p5_ambient(scene):
    """Distant city grid — Physical AI theme"""
    grid = NumberPlane(
        x_range=[-8, 8, 2],
        y_range=[-5, 5, 2],
        background_line_style={
            "stroke_color": P5_PHYSICAL,
            "stroke_width": 0.4,
            "stroke_opacity": 0.04
        },
        axis_config={"stroke_opacity": 0}
    )
    scene.add_to_back(grid)
```

---

## PHẦN G: SCENE-LEVEL CHOREOGRAPHY

### G1 — Scene Opening (mỗi body scene)

```python
def scene_open(scene: Scene, title: str, 
                part_color: str = CYAN_NEON,
                show_scan=True) -> None:
    """
    Standard opening cho mọi body scene — 3-beat choreography:
    Beat 1 (0.0s): Background "activates" — grid lines brighten briefly
    Beat 2 (0.4s): Title scans in (xem A1)
    Beat 3 (0.8s): Separator line draws
    
    Tổng: ~1.0s, sau đó main content bắt đầu
    """
    # Beat 1: BG activation
    bg_flash = BackgroundRectangle(
        scene.camera.frame, color=part_color, opacity=0.03
    )
    scene.play(FadeIn(bg_flash, run_time=0.15), 
               FadeOut(bg_flash, run_time=0.25))
    
    # Beat 2: Title
    title_mob = Text(title, font_size=SIZE_TITLE, 
                     color=TEXT_WHITE, font=FONT_PRIMARY)
    title_mob.to_edge(UP, buff=0.3)
    
    if show_scan:
        scan_line = Line(
            title_mob.get_left() + LEFT*0.1,
            title_mob.get_left() + LEFT*0.1,
            stroke_color=part_color, stroke_width=2.0
        )
        scene.play(
            AnimationGroup(
                scan_line.animate(run_time=0.6, rate_func=smooth)
                         .put_start_and_end_on(
                             title_mob.get_left(),
                             title_mob.get_right() + RIGHT*0.1
                         ),
                AddTextLetterByLetter(title_mob, run_time=0.55)
            )
        )
        scene.play(FadeOut(scan_line, run_time=0.15))
    else:
        scene.play(Write(title_mob, run_time=0.5))
    
    # Beat 3: Separator
    sep = Line(
        LEFT * 6.5, RIGHT * 6.5,
        stroke_color=part_color, stroke_width=0.8, stroke_opacity=0.35
    ).next_to(title_mob, DOWN, buff=0.15)
    
    scene.play(Create(sep, run_time=0.35, rate_func=smooth))
    
    return title_mob, sep
```

### G2 — Scene Close (mỗi body scene)

```python
def scene_close(scene: Scene, 
                 part_color: str = CYAN_NEON) -> None:
    """
    Standard close — 2-beat:
    Beat 1: Content fades out (keep title if transitioning)
    Beat 2: Brief color flash xác nhận scene kết thúc
    """
    content_mobs = [m for m in scene.mobjects 
                    if not isinstance(m, BackgroundRectangle)]
    
    if content_mobs:
        scene.play(
            LaggedStart(*[
                FadeOut(m, shift=UP*0.05) for m in content_mobs
            ], lag_ratio=0.04, run_time=0.5)
        )
    
    # Beat 2: brief flash
    flash = BackgroundRectangle(
        scene.camera.frame, color=part_color, opacity=0.04
    )
    scene.play(
        FadeIn(flash, run_time=0.1),
        FadeOut(flash, run_time=0.2)
    )
    scene.wait(0.1)
```

### G3 — "Key Insight" Moment (1-2 lần mỗi scene)

Khi presenter nói câu "punchline" — ý tưởng chốt của cả scene:

```python
def key_insight_reveal(text: str, 
                        scene: Scene,
                        color=GOLD) -> None:
    """
    "Punchline" animation — dùng tối đa 2 lần mỗi scene.
    
    1. Screen dims (overlay 20% opacity)
    2. Text appears center stage, large, gold
    3. Glow ring expands out from text
    4. Hold 2s
    5. Text fades, screen brightens back
    """
    dim_overlay = BackgroundRectangle(
        scene.camera.frame, color=BG_VOID, opacity=0.5
    )
    
    insight_text = Text(text, font_size=SIZE_BODY + 6,
                        color=color, font=FONT_PRIMARY,
                        line_spacing=1.4)
    insight_text.move_to(ORIGIN)
    
    glow_circle = Circle(
        radius=max(insight_text.width, insight_text.height) * 0.7,
        stroke_color=color, stroke_opacity=0, fill_opacity=0
    )
    glow_circle.move_to(ORIGIN)
    
    scene.play(
        FadeIn(dim_overlay, run_time=0.3),
        Write(insight_text, run_time=0.8),
    )
    scene.play(
        glow_circle.animate(run_time=0.6).scale(2.5).set_stroke(opacity=0.3),
        glow_circle.copy().animate(run_time=0.8).scale(3.5).set_stroke(opacity=0),
    )
    scene.wait(2.0)
    scene.play(
        FadeOut(dim_overlay, run_time=0.4),
        FadeOut(insight_text, run_time=0.4),
        FadeOut(glow_circle, run_time=0.2),
    )
```

---

## PHẦN H: ĐẶC BIỆT — MỖI PHẦN MỘT SIGNATURE MICRO-DETAIL

Mỗi part có một **micro-animation detail** xuất hiện nhiều lần trong part đó — không phải signature cảnh lớn, mà là recurring visual language.

### H1 — Part 1: "Neural Spark"

Khi một FM process data:

```python
def neural_spark(source: Mobject, target: Mobject, 
                  color=P1_FOUNDATION) -> Succession:
    """
    Micro-detail: tiny spark travels từ source → target khi 
    data flows through a model. Xuất hiện mỗi khi model "processes".
    Duration: ~0.4s — rất nhanh, nhưng adds life.
    """
    spark = Dot(radius=0.03, color=WHITE)
    spark.move_to(source.get_center())
    
    path = ArcBetweenPoints(
        source.get_center(), 
        target.get_center(),
        angle=np.random.choice([-0.5, 0.5]) * np.random.uniform(0.3, 0.7)
    )
    
    return Succession(
        MoveAlongPath(spark, path, run_time=0.3, rate_func=smooth),
        Flash(target.get_center(), color=color,
              flash_radius=0.12, num_lines=4, run_time=0.15),
        FadeOut(spark, run_time=0.05)
    )
```

### H2 — Part 2: "Signal Ping"

Radar/V2X signal confirmation:

```python
def signal_ping(position: np.ndarray, 
                 color=CYAN_NEON) -> AnimationGroup:
    """
    Expanding rings từ một điểm — "ping" nhận được signal.
    Dùng mỗi khi V2X data được received.
    3 rings, staggered, fade out. Duration: ~0.6s.
    """
    rings = [
        Circle(radius=0, stroke_color=color, 
               stroke_width=2.0 - i*0.5,
               stroke_opacity=0.8 - i*0.2)
        .move_to(position)
        for i in range(3)
    ]
    
    return LaggedStart(*[
        Succession(
            rings[i].animate(run_time=0.5, rate_func=rush_from)
                    .scale(4 + i).set_stroke(opacity=0)
        )
        for i in range(3)
    ], lag_ratio=0.15)
```

### H3 — Part 3: "Scan-to-Twin"

Reality being "scanned" into sim:

```python
def reality_scan(mob: Mobject, scan_color=P3_SIM) -> Succession:
    """
    Horizontal scan line sweeps across any object.
    Behind scan: "digital" version appears (sharper edges, grid texture).
    Duration: ~0.8s.
    """
    scan = Line(
        mob.get_left() + UP * mob.height/2,
        mob.get_right() + UP * mob.height/2,
        stroke_color=scan_color, stroke_width=3, stroke_opacity=0.9
    )
    
    digital_version = mob.copy().set_stroke(
        color=scan_color, width=0.8, opacity=0.4
    ).set_fill(color=BG_PANEL, opacity=0.9)
    digital_version.move_to(mob)
    
    return Succession(
        FadeIn(scan, run_time=0.1),
        AnimationGroup(
            scan.animate(run_time=0.6, rate_func=smooth)
                .shift(DOWN * mob.height),
            FadeIn(digital_version, run_time=0.5),
        ),
        FadeOut(scan, run_time=0.15),
    )
```

### H4 — Part 4: "Compression Squeeze"

Data being quantized/compressed:

```python
def compression_squeeze(mob: Mobject, 
                          target_scale=0.3,
                          target_color=INT8_LIGHT) -> Succession:
    """
    Object gets "squeezed" smaller, changes color to INT8_LIGHT.
    Green particle burst at end — "efficiency achieved".
    Duration: ~0.5s.
    """
    return Succession(
        mob.animate(run_time=0.3, rate_func=smooth)
           .scale(target_scale).set_color(target_color),
        Flash(mob.get_center(), color=target_color,
              flash_radius=0.2, num_lines=6, run_time=0.2),
        mob.animate(run_time=0.1).set_stroke(width=2)
    )
```

### H5 — Part 5: "Human Awareness"

Robot/AI "noticing" a human:

```python
def human_awareness(robot: Mobject, human: Mobject) -> Succession:
    """
    Robot's "attention" beam sweeps to find human.
    Line extends from robot → human, human brightens.
    Duration: ~0.7s.
    """
    attention_line = DashedLine(
        robot.get_center(),
        robot.get_center(),
        stroke_color=P5_PHYSICAL, stroke_width=1.5,
        stroke_opacity=0.6
    )
    
    return Succession(
        attention_line.animate(run_time=0.4)
                      .put_start_and_end_on(
                          robot.get_center(),
                          human.get_center()
                      ),
        AnimationGroup(
            human.animate(run_time=0.2).set_color(P5_PHYSICAL),
            Flash(human.get_center(), color=P5_PHYSICAL,
                  flash_radius=0.2, num_lines=5, run_time=0.2),
        ),
        FadeOut(attention_line, run_time=0.3)
    )
```

---

## PHẦN I: MASKING VÀ REVEAL TECHNIQUES

### I1 — Curtain Reveal (cho "before → after" transitions lớn)

```python
def curtain_reveal(hidden_content: VGroup, 
                    direction=RIGHT,
                    color=BG_SPACE) -> Succession:
    """
    Curtain wipes từ edge, revealing content behind.
    Dùng cho: before/after diagrams, solution reveals.
    """
    curtain = Rectangle(
        width=hidden_content.width + 0.5,
        height=hidden_content.height + 0.5,
        fill_color=color, fill_opacity=1,
        stroke_width=0
    ).move_to(hidden_content)
    
    return Succession(
        FadeIn(hidden_content, run_time=0.1),
        curtain.animate(run_time=0.7, rate_func=smooth)
               .shift(direction * (curtain.width + 0.5)),
        FadeOut(curtain, run_time=0.1)
    )
```

### I2 — Voxel Grid Reveal (cho CooPre masked reconstruction)

```python
def voxel_grid_reveal(n_rows=8, n_cols=8, 
                       mask_ratio=0.4,
                       cell_size=0.35) -> tuple[VGroup, VGroup, Succession]:
    """
    Returns: (all_voxels, masked_voxels, reveal_animation)
    
    Active voxels: VOXEL_ACTIVE color, full opacity
    Masked voxels: VOXEL_MASKED color, revealed gradually
    """
    all_voxels = VGroup()
    masked_indices = set(
        np.random.choice(n_rows * n_cols, 
                         int(n_rows * n_cols * mask_ratio), 
                         replace=False)
    )
    
    for i in range(n_rows):
        for j in range(n_cols):
            idx = i * n_cols + j
            is_masked = idx in masked_indices
            
            voxel = Square(
                side_length=cell_size * 0.9,
                fill_color=VOXEL_MASKED if is_masked else VOXEL_ACTIVE,
                fill_opacity=0.3 if is_masked else 0.6,
                stroke_color=GRID_LINE,
                stroke_width=0.5
            ).move_to([
                (j - n_cols/2 + 0.5) * cell_size,
                (i - n_rows/2 + 0.5) * cell_size,
                0
            ])
            all_voxels.add(voxel)
    
    masked_voxels = VGroup(*[
        all_voxels[i] for i in masked_indices
    ])
    
    # Appearance animation
    initial_reveal = LaggedStart(*[
        GrowFromCenter(v, run_time=0.05)
        for v in all_voxels
    ], lag_ratio=0.02)
    
    # Mask dropout (active → masked color)
    mask_anims = LaggedStart(*[
        all_voxels[i].animate(run_time=0.15)
                     .set_fill(VOXEL_MASKED, opacity=0.2)
        for i in masked_indices
    ], lag_ratio=0.04)
    
    reveal_anim = Succession(initial_reveal, mask_anims)
    
    return all_voxels, masked_voxels, reveal_anim
```

---

## PHẦN J: TIMELINE / SEQUENCE DIAGRAMS

### J1 — Method Evolution Timeline (V2VNet → CodeFilling, etc.)

```python
def evolution_timeline(
    milestones: list[dict],
    # Each dict: {"year": 2020, "name": "V2VNet", 
    #              "contribution": "GNN fusion",
    #              "bottleneck": "fusion quality",
    #              "color": BLUE_ELECTRIC}
) -> Succession:
    """
    Timeline với chain of causality:
    Each method appears và labels WHY the next one was needed.
    NO zigzag — all labels ABOVE the timeline spine.
    """
    n = len(milestones)
    spine_width = min(12.0, n * 2.8)
    spacing = spine_width / (n - 1)
    
    spine = Line(
        LEFT * spine_width/2,
        RIGHT * spine_width/2,
        stroke_color=TEXT_GHOST, stroke_width=1.2
    ).shift(DOWN * 0.5)
    
    nodes = []
    node_labels = []
    year_labels = []
    contrib_labels = []
    bottleneck_arrows = []
    
    for i, ms in enumerate(milestones):
        x = -spine_width/2 + i * spacing
        
        # Node circle
        node = Circle(
            radius=0.18,
            fill_color=ms["color"],
            fill_opacity=1.0,
            stroke_color=TEXT_WHITE,
            stroke_width=1.5
        ).move_to([x, -0.5, 0])
        nodes.append(node)
        
        # Method name ABOVE spine
        name = Text(ms["name"], font_size=SIZE_LABEL, 
                    color=ms["color"], weight=BOLD)
        name.move_to([x, 0.3, 0])
        node_labels.append(name)
        
        # Year BELOW spine
        year = Text(str(ms["year"]), font_size=SIZE_MICRO, color=TEXT_DIM)
        year.move_to([x, -1.0, 0])
        year_labels.append(year)
        
        # Contribution (short) — above name
        contrib = Text(ms["contribution"], font_size=SIZE_MICRO,
                       color=TEXT_DIM, slant=ITALIC)
        contrib.move_to([x, 0.7, 0])
        contrib_labels.append(contrib)
    
    # Bottleneck arrows between nodes (pointing to why next exists)
    for i in range(n - 1):
        # "addresses" text midway
        mid_x = (-spine_width/2 + (i + 0.5) * spacing)
        bottleneck = Text(
            f"→ addresses:\n'{milestones[i]['bottleneck']}'",
            font_size=SIZE_MICRO, color=TEXT_DIM, slant=ITALIC,
            line_spacing=0.8
        ).move_to([mid_x, -1.5, 0])
        bottleneck_arrows.append(bottleneck)
    
    # Build animation
    anims = []
    
    # Spine first
    anims.append(Create(spine, run_time=0.6, rate_func=smooth))
    
    # Each milestone
    for i in range(n):
        milestone_entrance = Succession(
            GrowFromCenter(nodes[i], run_time=0.2),
            Flash(nodes[i].get_center(), 
                  color=milestones[i]["color"],
                  flash_radius=0.3, num_lines=6, run_time=0.2),
            AnimationGroup(
                FadeIn(node_labels[i], shift=UP*0.1, run_time=0.25),
                FadeIn(contrib_labels[i], shift=UP*0.05, run_time=0.2),
                FadeIn(year_labels[i], shift=DOWN*0.05, run_time=0.2),
            )
        )
        anims.append(milestone_entrance)
        
        # Bottleneck text between milestones
        if i < n - 1:
            anims.append(
                FadeIn(bottleneck_arrows[i], shift=UP*0.05, run_time=0.3)
            )
    
    return Succession(*anims)
```

---

## PHẦN K: CAMERA MOVES

### K1 — Rack Focus (zoom in on key element)

```python
def rack_focus(scene: Scene, target: Mobject,
                zoom_factor=1.8, duration=0.7) -> None:
    """
    Camera zooms in on target while non-target content dims.
    Dùng để emphasize một element trong diagram.
    """
    # Dim everything except target
    other_mobs = [m for m in scene.mobjects 
                  if m is not target and not isinstance(m, BackgroundRectangle)]
    
    frame = scene.camera.frame
    
    scene.play(
        AnimationGroup(
            frame.animate(run_time=duration, rate_func=smooth)
                 .set(width=frame.width / zoom_factor)
                 .move_to(target),
            *[m.animate(run_time=duration).set_opacity(0.2)
              for m in other_mobs]
        )
    )

def rack_unfocus(scene: Scene, duration=0.5) -> None:
    """Pull back out, restore opacity"""
    frame = scene.camera.frame
    other_mobs = [m for m in scene.mobjects 
                  if not isinstance(m, BackgroundRectangle)]
    
    scene.play(
        AnimationGroup(
            frame.animate(run_time=duration).set(width=14.22).move_to(ORIGIN),
            *[m.animate(run_time=duration).set_opacity(1.0)
              for m in other_mobs]
        )
    )
```

### K2 — Part Transition Camera Wipe

```python
def part_wipe_transition(scene: Scene, 
                          direction=LEFT,
                          new_bg_color=BG_VOID) -> None:
    """
    Màn hình wipes ra theo direction, revealing part title card background.
    Mượt hơn simple FadeToColor.
    """
    wipe_rect = Rectangle(
        width=0.1, height=10,
        fill_color=new_bg_color, fill_opacity=1,
        stroke_width=0
    )
    
    if direction == LEFT:
        wipe_rect.to_edge(RIGHT, buff=-0.1)
    else:
        wipe_rect.to_edge(LEFT, buff=-0.1)
    
    scene.play(
        wipe_rect.animate(run_time=0.6, rate_func=smooth)
                 .set(width=16).move_to(ORIGIN)
    )
```

---

## QUICK REFERENCE CHEAT SHEET

```
Element                  → Animation Recipe
─────────────────────────────────────────────────────
Scene title              → A1: scan_line reveal
Part title               → A2: forge_text
Body text (paragraph)    → A3: line-by-line slide in
Key term (first mention) → A4: gold reveal + underline + glow
Stats/numbers            → A5: counter + milestone burst
Bullet list              → A6: dot flash + letterbyLetter
Key quotes               → A7: frame lines + word-by-word
Citation footnote        → A8: subtle drift-up
Pipeline block           → B1: corners → border → fill flood → label scan
Info panel               → B2: border + scan sweep + shimmer
Result box               → B3: stamp + checkmark flash
Before/after             → B4: dim before, curtain divider, bright after
Neural net block         → B5: internal shimmer dots
Standard arrow           → C1 "electric": fast Create + tip flash
V2X comm link            → C2: dashed line + hexagon packets
Error cascade            → C3: red flash + shake per arrow
Axes                     → D1: origin flash + X/Y shoot + ticks + labels
Bar chart bar            → D2: grow + particle trail + counter + lock flash
Curve/line               → D3: glowing head traces + afterglow
Scatter points           → D4: rain / burst / scan (choose by context)
Power-law curve          → D5: trace + area + tail highlight + pulse
Car icon                 → E1: drive in from edge + rolling wheels
Building                 → E2: drop from sky + dust impact
Checkmark                → E3: stamp + ring expand
FM hexagon icons         → E4: grow + wire connect + float updater
Background (body)        → F1: particle drift (25 particles)
Background P1            → F2: faint neural net
Background P2            → F2: faint radar rings
Background P4            → F2: falling binary digits
Background P5            → F2: faint city grid
Every scene start        → G1: BG flash + title scan + separator
Every scene end          → G2: content fade + part-color flash
Punchline/key insight    → G3: dim overlay + center text + glow ring
Part 1 micro             → H1: neural spark (0.4s, recurring)
Part 2 micro             → H2: signal ping (0.6s, recurring)
Part 3 micro             → H3: scan-to-twin (0.8s, recurring)
Part 4 micro             → H4: compression squeeze (0.5s, recurring)
Part 5 micro             → H5: human awareness beam (0.7s, recurring)
Curtain reveal           → I1: curtain wipes off
Voxel grid               → I2: grow + mask dropout
Method timeline          → J1: spine + nodes + labels ABOVE + bottleneck text
Zoom emphasis            → K1: rack_focus / rack_unfocus
Part transition          → K2: wipe rect
```

---

## TIMING REFERENCE

```
Element type             Min duration    Max duration    Notes
─────────────────────────────────────────────────────────────────
Scene title              0.8s            1.0s            
Body text (1 line)       0.3s            0.5s            
Body text (paragraph)    0.5s            0.8s            
Key term reveal          0.5s            0.7s            
Quote reveal             1.5s            2.5s            + 2s hold after
Counter animation        1.2s            2.0s            
Pipeline block           0.6s            0.9s            
Info panel               0.8s            1.2s            
Arrow (electric)         0.3s            0.4s            
Arrow (data stream)      0.7s            1.0s            
Axes deploy              0.8s            1.2s            
Bar grow                 1.0s            1.5s            
Curve trace              1.2s            2.0s            
Car entrance             0.8s            1.0s            
Signal ping              0.5s            0.6s            
Neural spark             0.35s           0.45s           
Key insight              4.0s            6.0s            incl hold
Scene open (total)       0.9s            1.1s            
Scene close (total)      0.6s            0.8s            
Wait after punchline     1.5s            2.5s            mandatory
```

---

*File này bổ sung cho BEYOND_SELFDRIVING_ANIMATION_GUIDE.md — đọc cả hai trước khi code.*
*Nếu một animation type không có trong file này → hỏi trước khi tự improvise.*
