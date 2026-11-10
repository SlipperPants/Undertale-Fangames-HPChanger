# Undertale Fangames - HPchanger (Demo)

---

## [EN]

A simple Python tool I made to change HP in Undertale fan games without dealing with Cheat Engine every time. It automatically detects the game and its engine (GameMaker, Clickteam, Unity/CYF, Kristal, Godot).

### How to use
You don't need to click the app window while playing. Even if the game locks your mouse, just use your keyboard inside the game:

1. Press **`V`** to clear the box, then type your current HP (e.g. `92`) using number keys.
2. Press **`B`** to scan.
3. Take damage once in the game so your HP drops.
4. Press **`V`**, type your new HP, and press **`N`** to find the address.
5. Press **`M`** to set your HP to `99999`.

**Extra mechanics:**
* **`O` (Auto-Heal):** Refreshes your HP every millisecond (1ms). Use this if the game caps your max HP at 92 or has Karma (KR) poison drain.
* **`P` (Freeze Game):** Freezes the whole game mid-attack so bullets stop moving while you scan your HP. Press `P` again to unfreeze.
* **Custom Keys & Language:** You can change any of the `V-B-N-M-O-P` keys at the bottom or turn hotkeys off. Your settings are saved automatically in `settings.json`. Top-right button switches between `EN` and `TR`.

### Notes
* **Demo version:** This is still a demo and I haven't tested it on every fan game out there, so bugs might happen in some games.
* **Not a virus:** It's just a single open-source `.py` file with no extra libraries. Since it reads/writes game RAM like Cheat Engine, Windows or antivirus programs might give a false warning if you turn it into an `.exe`. You can open `HPchanger.py` with Notepad to check the code yourself.

---

## [TR]

Undertale fan oyunlarında her seferinde Cheat Engine ile uğraşmamak için yaptığım basit bir can (HP) değiştirme aracı. Açtığınız oyunu ve hangi motorla yapıldığını (GameMaker, Clickteam, Unity/CYF, Kristal, Godot) otomatik algılar.

### Nasıl kullanılır?
Oyun açıkken programa tıklamanıza gerek yok. Gaster/Sans gibi savaşlarda mouse kilitlense bile oyunun içindeyken direkt klavyeden yapabilirsiniz:

1. **`V`** tuşuna basıp kutuyu silin, klavyeden o anki canınızı (örn. `92`) tuşlayın.
2. **`B`** tuşuna basıp ilk taramayı yapın.
3. Oyunda 1 kere hasar alın.
4. Tekrar **`V`** basıp yeni düşen canınızı yazın ve **`N`** tuşuna basarak adresi bulun.
5. **`M`** tuşuna basarak canınızı `99999` yapın.

**Ekstra özellikler:**
* **`O` (Oto-Yenile):** Canı her milisaniye (1ms) yeniler. Maksimum can sınırı (92 sınırı gibi) veya Karma (KR) hasarı olan oyunlarda ölmemek için açabilirsiniz.
* **`P` (Oyunu Dondur):** Sıra tabanlı olmayan saldırılarda oyunu ve mermileri havada dondurur. Rahatça tarama yapıp tekrar `P` ile oyunu devam ettirebilirsiniz.
* **Tuş Değiştirme ve Dil:** En alttaki kutulardan `V-B-N-M-O-P` tuşlarını istediğiniz harfle değiştirebilir veya kısayolları kapatabilirsiniz. Yaptığınız ayarlar `settings.json` dosyasına kaydedilir, sıfırlanmaz. Sağ üstten `TR` / `EN` dil seçebilirsiniz.

### Notlar
* **Demo sürümü:** Araç şu an demo aşamasında ve piyasadaki tüm fan oyunlarında denenmedi. Bazı oyunlarda çalışmayabilir veya hata verebilir.
* **Virüs değildir:** Kodun tamamı tek bir `.py` dosyası içinde açık kaynaklıdır ve dışarıdan hiçbir kütüphane kullanmaz. Oyunun RAM'ine müdahale ettiği için antivirüsler bazen uyarı verebilir, dosyayı Not Defteri ile açıp kodlara kendiniz bakabilirsiniz.
