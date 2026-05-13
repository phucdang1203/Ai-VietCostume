# app/pipeline/prompt_service.py

import random
from typing import Dict

class PromptService:
    """
    Dịch vụ tạo Prompt chuyên sâu: 
    - Ràng buộc logic Giai cấp - Vật dụng - Trang phục.
    - Phong cách Cinematic Card Game (Góc máy trung cảnh).
    """

    # Định nghĩa cấu trúc dữ liệu theo Giai cấp (Archetypes)
    ARCHETYPES = {
        "Royalty": {  # HOÀNG GIA / VƯƠNG TỘC
            "man": {
                "robes": [
                    "imperial gold Áo Giao Lĩnh with five-clawed dragon embroidery",
                    "golden Long bào with royal dragon insignia",
                    "ceremonial Áo Cổn Miện with celestial embroidery",
                    "luxury yellow Áo Tấc for grand court rituals",
                    "royal silk Áo Viên Lĩnh with cloud motifs",
                    "imperial brocade robe with Đông Sơn-inspired patterns",
                    "red ceremonial court robe with gold-thread dragons",
                    "high-ranking Nguyễn dynasty formal robe",
                    "royal woven silk robe with phoenix-dragon balance",
                    "grand palace robe with sacred mountain motifs"
                ],
                "heads": [
                    "golden Miện crown",
                    "ornate Mão Bình Thiên",
                    "luxury Khăn Xếp",
                    "imperial golden headpiece with jade",
                    "royal Mão Cửu Long",
                    "formal Khăn Đóng with gold trim",
                    "dragon-engraved ceremonial crown",
                    "royal silk headdress"
                ],
                "items": [
                    "Ngọc Tỷ imperial jade seal",
                    "gold-hilted royal sword",
                    "yellow silk royal decree scroll",
                    "jade Hốt tablet",
                    "luxury white silk fan with calligraphy",
                    "royal jade pendant",
                    "ceremonial dragon staff",
                    "golden ancestral tablet",
                    "imperial incense holder",
                    "precious court beads"
                ]
            },
            "woman": {
                "robes": [
                    "red Áo Nhật Bình with phoenix embroidery",
                    "yellow imperial Áo Nhật Bình with silk ribbons",
                    "royal Phượng bào with golden phoenixes",
                    "luxury Áo Ngũ Thân court dress",
                    "ceremonial red Áo Tấc",
                    "palace silk gown with lotus motifs",
                    "royal embroidered robe with peacock feather patterns",
                    "gold-threaded imperial gown",
                    "formal Nguyễn dynasty queen attire",
                    "elegant court robe with sacred floral designs"
                ],
                "heads": [
                    "golden Trâm Phượng hairpins",
                    "royal Phượng Quan",
                    "luxury pearl royal headpiece",
                    "golden Mấn hoàng gia",
                    "jade-encrusted palace crown",
                    "ornate silk headdress",
                    "phoenix tassel crown",
                    "courtly jewel hair ornaments"
                ],
                "items": [
                    "royal silk fan with peacock feathers",
                    "gold handheld mirror",
                    "jade Như Ý scepter",
                    "embroidered royal silk handkerchief",
                    "gold jewelry box",
                    "luxury perfume sachet",
                    "ceremonial lotus fan",
                    "royal bead necklace",
                    "palace flower basket",
                    "precious jade bracelet"
                ]
            }
        },

        "Mandarin": {  # QUAN LẠI
            "man": {
                "robes": [
                    "purple official Áo Ngũ Thân",
                    "dark blue mandarin robe with Bổ Tử rank badge",
                    "formal Áo Tấc for civil service",
                    "black silk Áo Viên Lĩnh",
                    "traditional court robe with crane insignia",
                    "embroidered official garment with scholarly motifs",
                    "dark ceremonial robe for royal administration",
                    "luxury brocade bureaucratic robe",
                    "high-ranking court attire",
                    "formal Nguyễn dynasty administrative robe"
                ],
                "heads": [
                    "Official Phốc Đầu hat",
                    "black Khăn Xếp",
                    "Mũ Cánh Chuồn",
                    "traditional Khăn Đóng",
                    "formal silk bureaucratic headdress",
                    "court-ranking official hat",
                    "luxury ceremonial headwear"
                ],
                "items": [
                    "wooden Hốt tablet",
                    "calligraphy brush",
                    "administrative scroll bundle",
                    "luxury sandalwood fan",
                    "ink stone",
                    "official seal",
                    "bureaucratic ledger",
                    "ceremonial rank tablet",
                    "silk decree holder",
                    "court documentation case"
                ]
            },
            "woman": {
                "robes": [
                    "elegant Áo Ngũ Thân with noble embroidery",
                    "dark green Áo Nhật Bình",
                    "formal silk Áo Tấc",
                    "luxury court lady robe",
                    "purple noblewoman gown",
                    "embroidered silk ceremonial attire",
                    "traditional aristocratic household robe"
                ],
                "heads": [
                    "gold hairpins with jade",
                    "Khăn Lươn",
                    "silk Khăn Vấn",
                    "noblewoman Mấn",
                    "formal household headdress"
                ],
                "items": [
                    "lacquer jewelry box",
                    "silk lotus fan",
                    "prayer beads",
                    "embroidery frame",
                    "poetry scroll",
                    "jade bracelet",
                    "decorative flower basket"
                ]
            }
        },

        "Military": {  # QUÂN ĐỘI
            "man": {
                "robes": [
                    "Lê-Trịnh dynasty leather armor over red tunic",
                    "iron-plated brigandine armor",
                    "traditional silk military tunic",
                    "Đông Sơn-inspired bronze chest armor",
                    "battle robe with tiger insignia",
                    "lamellar warrior armor",
                    "royal guard combat attire",
                    "heavy battlefield command armor",
                    "light infantry woven armor",
                    "ceremonial general battle robe"
                ],
                "heads": [
                    "bronze war helmet",
                    "red military headband",
                    "traditional conical war hat",
                    "general’s plumed helmet",
                    "reinforced leather battle cap",
                    "bronze crested helmet",
                    "combat Khăn Vấn"
                ],
                "items": [
                    "sharp steel Gươm",
                    "traditional Giáo spear",
                    "bronze shield",
                    "military command flag",
                    "battle-ready Đại đao",
                    "crossbow",
                    "war drum",
                    "bronze axe",
                    "ceremonial command baton",
                    "curved cavalry blade",
                    "iron mace",
                    "bamboo spear"
                ]
            },
            "woman": {
                "robes": [
                    "female warrior light armor",
                    "embroidered silk tunic with leather braces",
                    "Trưng Sisters-inspired battle attire",
                    "light cavalry robe",
                    "heroic resistance warrior garment"
                ],
                "heads": [
                    "red silk headband",
                    "silver warrior hairpin",
                    "combat headdress",
                    "light bronze battle cap"
                ],
                "items": [
                    "dual swords",
                    "traditional recurve bow",
                    "military signaling horn",
                    "battle spear",
                    "light shield",
                    "ceremonial resistance flag"
                ]
            }
        },

        "Scholar": {  # TRÍ THỨC / NHO SĨ
            "man": {
                "robes": [
                    "simple white Áo Ngũ Thân",
                    "light blue silk scholar robe",
                    "black Áo the",
                    "traditional Confucian robe",
                    "plain scholarly Áo Giao Lĩnh",
                    "modest educational court robe",
                    "bookman’s silk attire"
                ],
                "heads": [
                    "black Khăn Xếp",
                    "simple bamboo hair pin",
                    "scholar’s Khăn Đóng",
                    "traditional literary cap"
                ],
                "items": [
                    "bamboo scroll of Confucian classics",
                    "ink stone",
                    "bamboo fan",
                    "cloth bag of books",
                    "calligraphy brush",
                    "paper scroll bundle",
                    "poetry manuscript"
                ]
            },
            "woman": {
                "robes": [
                    "pastel Áo Ngũ Thân",
                    "simple silk robe",
                    "elegant Áo Tứ Thân",
                    "Yếm đào with scholarly modesty",
                    "traditional literary woman attire"
                ],
                "heads": [
                    "pearl hair pin",
                    "traditional bun",
                    "simple silk scarf"
                ],
                "items": [
                    "poem book",
                    "flower branch",
                    "silk embroidery frame",
                    "lotus fan",
                    "calligraphy set"
                ]
            }
        },

        "Commoner": {  # DÂN THƯỜNG / NÔNG DÂN
            "man": {
                "robes": [
                    "rustic brown Áo Cánh",
                    "simple hemp fabric clothes",
                    "grey coarse linen tunic",
                    "traditional Áo Bà Ba",
                    "plain field worker attire",
                    "mud-dyed farming clothes",
                    "woven rural garment",
                    "simple indigo tunic"
                ],
                "heads": [
                    "worn-out Nón Lá",
                    "simple fabric headband",
                    "bare head with top knot",
                    "Khăn Rằn",
                    "farmer’s cloth wrap"
                ],
                "items": [
                    "Điếu cày",
                    "wooden walking stick",
                    "fishing net",
                    "bamboo basket",
                    "farming sickle",
                    "rice harvesting knife",
                    "bamboo water container",
                    "carrying pole",
                    "woven fish trap",
                    "oil lamp"
                ]
            },
            "woman": {
                "robes": [
                    "brown Áo Tứ Thân",
                    "traditional Yếm đào with dark wrap skirt",
                    "simple linen tunic",
                    "Áo Bà Ba",
                    "rural silk blouse",
                    "woven peasant attire",
                    "traditional market-day clothing"
                ],
                "heads": [
                    "Nón Quai Thao",
                    "Khăn Mỏ Quạ",
                    "simple cloth wrap",
                    "traditional village scarf"
                ],
                "items": [
                    "bamboo vegetable basket",
                    "lotus flower",
                    "traditional oil lamp",
                    "small clay pot",
                    "woven carrying basket",
                    "rice tray",
                    "market goods pole",
                    "silk sash pouch"
                ]
            }
        }
    }

    # Bối cảnh (Backgrounds)
    MOODS = [
        "inside a grand royal palace with golden pillars",
        "ancient Citadel gate with stone carvings",
        "misty traditional village garden with bamboo",
        "ancient temple courtyard with incense smoke",
        "historical library with candlelight and scrolls",
        "rustic riverside with a wooden boat"
    ]

    # Cập nhật Negative Prompt: Siết chặt để chặn phong cách 2D, minh họa
    NEGATIVE_PROMPT = (
        "earrings on men, makeup on men, feminine features on men, "
        "cartoon, anime, illustration, painting, drawing, vector, watercolor, flat design, 2d, " # Chặn triệt để 2D
        "low resolution, blur, deformed face, bad anatomy, distorted hands, extra fingers, "
        "western clothing, jeans, wristwatch, sunglasses, camera, modern buildings, modern furniture, "
        "chinese hanfu, korean hanbok, japanese kimono"
    )

    def _get_age_group(self, age: int) -> str:
        if age < 32: return "young"
        elif age < 55: return "middle-aged"
        return "elderly"

    def generate_prompt(self, gender: str, age: int) -> Dict[str, str]:
        g_key = "woman" if gender.lower() == "woman" else "man"
        a_desc = self._get_age_group(age)
        
        # 1. Chọn Giai cấp ngẫu nhiên
        rank = random.choice(list(self.ARCHETYPES.keys()))
        data = self.ARCHETYPES[rank][g_key]
        
        # 2. Chọn các thành phần ĐÚNG LOGIC giai cấp
        robe = random.choice(data["robes"])
        head = random.choice(data["heads"])
        item = random.choice(data["items"])
        mood = random.choice(self.MOODS)

        # 3. Kết hợp thành Prompt phong cách Card Game
        # --- BƯỚC 3 CẬP NHẬT: THAY ĐỔI PHONG CÁCH TỪ MINH HỌA SANG NHIẾP ẢNH 3D CHÂN THỰC ---
        # Bố cục: [Phong cách nhiếp ảnh] + [Nhân vật/Góc máy] + [Trang phục] + [Vật dụng] + [Ánh sáng/Bối cảnh]
        # --- CẬP NHẬT: ÉP GÓC MÁY TỪ ĐẦU GỐI TRỞ LÊN (MEDIUM-LONG SHOT) ---
        # --- BẢN CẬP NHẬT CUỐI: GIỮ NGUYÊN ĐẦU + NHÌN THẲNG + GÓC TRÊN ĐẦU GỐI ---
        full_prompt = (
            f"Hyper-realistic 2k photograph, cinematic film still. "
            f"Medium-long shot, shot from the knees up, looking at camera, head-on view. " # Nhìn thẳng camera
            f"Full head visible, wide head room, top of head not cropped. " # Giữ nguyên phần đầu, không bị cắt
            f"A {a_desc} Vietnamese {g_key} standing centered, representing the {rank} class. "
            f"Facing forward, front view, wearing {robe}, {head} on head. " # Hướng mặt về phía trước
            f"Hands clearly visible {item}. Detailed expressive face, sharp focus on eyes. "
            f"Historical Dai Viet era style, authentic Vietnamese aesthetics, background of {mood}. "
            f"Intricate fabric textures, realistic skin, volumetric lighting, dramatic backlighting, "
            f"masterpiece, sharp focus, 3d depth of field, cinematic color grading."
        )
        # ------------------------------------------------------------------

        return {
            "occupation": rank,
            "age_group": a_desc,
            "gender": g_key,
            "prompt": full_prompt,
            "negative_prompt": self.NEGATIVE_PROMPT
        }
    
# import random
# from typing import Dict

# class PromptService:
#     """
#     Dịch vụ tạo Prompt chuyên sâu về cổ phục Việt Nam.
#     Tối ưu hóa hiển thị TOÀN THÂN và phân biệt GIỚI TÍNH nghiêm ngặt.
#     """

#     # Hệ thống định nghĩa trang phục chi tiết (Hơn 10 định nghĩa mỗi giới tính)
#     COSTUME_DATABASE = {
#         "man": {
#             "young": [
#                 {"rank": "Royalty_Prince", "desc": "young Vietnamese prince, full body shot, masculine pose, luxury gold silk Giao Linh robe, long silk trousers, royal boots, high-class silk, no earrings"},
#                 {"rank": "Scholar", "desc": "young Vietnamese male scholar, full body shot, clean-shaven, elegant white Ao Ngu Than, traditional black headscarf, holding a bamboo scroll, traditional cloth shoes"},
#                 {"rank": "Military_General", "desc": "young Vietnamese male general, full body shot, heroic stance, traditional leather and metal armor, silk inner tunic, holding a sword, masculine energy"},
#                 {"rank": "Commoner_Villager", "desc": "young Vietnamese man, full body shot, brown silk Ao Canh, short pants, rustic look, energetic, traditional masculine appearance"},
#                 {"rank": "Palace_Guard", "desc": "young Vietnamese palace guard, full body shot, standing straight, red and yellow uniform, holding a spear, traditional conical hat"},
#                 {"rank": "Noble_Man", "desc": "young Vietnamese nobleman, full body shot, dark blue Ao Ngu Than, luxury fabric, holding a traditional fan, wealthy appearance"}
#             ],
#             "middle": [
#                 {"rank": "High_Mandarin", "desc": "mature Vietnamese male mandarin, full body shot, official violet brocade robe, large Bo Tu embroidery on chest, official tall hat, dignified short beard"},
#                 {"rank": "Merchant_Master", "desc": "successful Vietnamese male merchant, full body shot, rich patterned silk Ao Ngu Than, holding silver coins or silk rolls, prosperous look"},
#                 {"rank": "Physician", "desc": "mature Vietnamese male physician, full body shot, simple grey Ao Ngu Than, traditional medicine bag, wise and calm appearance"},
#                 {"rank": "Landowner", "desc": "mature Vietnamese landowner, full body shot, high quality brown silk robe, holding a walking stick, authoritative posture"}
#             ],
#             "old": [
#                 {"rank": "Village_Elder", "desc": "wise Vietnamese male patriarch, full body shot, silver beard, traditional simple grey silk robe, leaning on a wooden staff, serene expression"},
#                 {"rank": "Zen_Master", "desc": "elderly Vietnamese male zen master, full body shot, traditional brown monastic robe, Buddhist beads, peaceful wrinkled face, barefoot"}
#             ]
#         },
#         "woman": {
#             "young": [
#                 {"rank": "Royalty_Princess", "desc": "young Vietnamese princess, full body shot, vibrant red Nhat Binh robe, royal phoenix embroidery, gold hairpins, youthful elegant glow"},
#                 {"rank": "Noble_Lady", "desc": "young Vietnamese noble lady, full body shot, pastel silk Ao Ngu Than, pearl necklace, traditional flower hairpins, graceful beauty"},
#                 {"rank": "Commoner_Girl", "desc": "young Vietnamese girl, full body shot, vibrant Ao Tu Than, traditional pink yếm, silk headscarf, youthful radiant face"},
#                 {"rank": "Artiste", "desc": "young Vietnamese female performer, full body shot, colorful layered silk dress, holding a traditional Quai Thao hat, delicate traditional style"}
#             ],
#             "middle": [
#                 {"rank": "Noble_Matriarch", "desc": "mature noble lady, full body shot, dignified dark green Nhat Binh robe, royal jewelry, sophisticated traditional hairstyle"},
#                 {"rank": "Merchant_Woman", "desc": "mature Vietnamese female merchant, full body shot, elegant silk Ao Ngu Than, wealthy appearance, holding embroidery fabric"}
#             ],
#             "old": [
#                 {"rank": "Kind_Grandmother", "desc": "kind Vietnamese grandmother, full body shot, traditional brown Ao Tu Than, silver hair in a bun, chewing betel, gentle wrinkled face"}
#             ]
#         }
#     }

#     # Siết chặt Negative Prompt để tránh bông tai và trang phục nữ cho nam
#     NEGATIVE_PROMPT = (
#         "earrings, jewelry on men, makeup on men, long eyelashes on men, feminine features on men, "
#         "skirt, dress on men, bra, female underwear, "
#         "modern clothes, jeans, t-shirt, sunglasses, wristwatch, "
#         "cartoon, anime, 3d render, deformed, blurry, bad anatomy, extra fingers, "
#         "wrinkles on young skin, beard on woman, messy hair, low resolution, "
#         "crowded background, modern buildings, cars"
#     )

#     def _get_age_group(self, age: int) -> str:
#         if age < 32:
#             return "young"
#         elif 32 <= age < 55:
#             return "middle"
#         else:
#             return "old"

#     def generate_prompt(self, gender: str, age: int) -> Dict[str, str]:
#         """
#         Tạo prompt dựa trên giới tính và tuổi thực tế, ép buộc hiển thị toàn thân.
#         """
#         g_key = "woman" if gender.lower() == "woman" else "man"
#         a_group = self._get_age_group(age)
        
#         available_costumes = self.COSTUME_DATABASE[g_key][a_group]
#         selected = random.choice(available_costumes)
        
#         # Xây dựng prompt: Thay 'portrait' bằng 'full body shot' và thêm 'plain background'
#         full_prompt = (
#             f"masterpiece, 2k, {selected['desc']}, age {age} years old, "
#             f"historical Dai Viet period, standing on a plain white studio background, "
#             "cinematic lighting, highly detailed fabric texture, realistic skin, "
#             "shot on 35mm lens, full body view from head to toe"
#         )

#         return {
#             "occupation": selected["rank"],
#             "age_group": a_group,
#             "gender": g_key,
#             "prompt": full_prompt,
#             "negative_prompt": self.NEGATIVE_PROMPT
#         }
