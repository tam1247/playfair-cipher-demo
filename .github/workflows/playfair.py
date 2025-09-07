import string

# -------------------------------
# Tạo ma trận khóa 5x5
# -------------------------------
def generate_key_matrix(key: str):
    key = key.upper().replace("J", "I")  # gộp I và J
    seen = set()
    matrix = []

    for ch in key + string.ascii_uppercase:
        if ch.isalpha() and ch not in seen:
            seen.add(ch)
            matrix.append(ch)

    # trả về 5x5 (A-Z trừ J)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

# -------------------------------
# Tìm vị trí ký tự trong ma trận
# -------------------------------
def find_position(matrix, ch):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == ch:
                return row, col
    return None

# -------------------------------
# Tiền xử lý Plaintext thành cặp
# -------------------------------
def preprocess_text(text: str):
    text = text.upper().replace("J", "I")
    result = []
    i = 0
    while i < len(text):
        ch1 = text[i]
        if not ch1.isalpha():
            i += 1
            continue
        # tìm ch2 hợp lệ (bỏ ký tự không phải chữ)
        j = i + 1
        while j < len(text) and not text[j].isalpha():
            j += 1
        ch2 = text[j] if j < len(text) else None

        if ch2 is None:
            result.append((ch1, "X"))
            i += 1
        else:
            if ch1 == ch2:
                result.append((ch1, "X"))
                i += 1
            else:
                result.append((ch1, ch2))
                # nhảy tới vị trí sau ch2 trong chuỗi ban đầu
                i = j + 1
    return result

# -------------------------------
# Tách cipher thành cặp
# -------------------------------
def decrypt_pairs(cipher: str):
    cipher = cipher.upper()
    pairs = []
    i = 0
    while i < len(cipher):
        a = cipher[i]
        b = cipher[i+1] if i+1 < len(cipher) else 'X'
        pairs.append((a, b))
        i += 2
    return pairs

# -------------------------------
# Hàm mã hóa Playfair
# -------------------------------
def playfair_encrypt(plaintext: str, key: str):
    matrix = generate_key_matrix(key)
    print("\nMa trận khóa 5x5:")
    for row in matrix:
        print(" ".join(row))
    print("\nChia plaintext thành cặp:")

    pairs = preprocess_text(plaintext)
    for a, b in pairs:
        print(a + b, end=" ")
    print("\n")

    cipher = ""
    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # cùng hàng -> shift phải
            cipher += matrix[row1][(col1+1) % 5]
            cipher += matrix[row2][(col2+1) % 5]
        elif col1 == col2:  # cùng cột -> shift xuống
            cipher += matrix[(row1+1) % 5][col1]
            cipher += matrix[(row2+1) % 5][col2]
        else:  # hình chữ nhật
            cipher += matrix[row1][col2]
            cipher += matrix[row2][col1]
    return cipher

# -------------------------------
# Hàm giải mã Playfair
# -------------------------------
def playfair_decrypt(cipher: str, key: str):
    matrix = generate_key_matrix(key)
    pairs = decrypt_pairs(cipher)
    print("\nChia cipher thành cặp:")
    for a, b in pairs:
        print(a + b, end=" ")
    print("\n")

    plain = ""
    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:  # cùng hàng -> shift trái
            plain += matrix[row1][(col1-1) % 5]
            plain += matrix[row2][(col2-1) % 5]
        elif col1 == col2:  # cùng cột -> shift lên
            plain += matrix[(row1-1) % 5][col1]
            plain += matrix[(row2-1) % 5][col2]
        else:  # hình chữ nhật
            plain += matrix[row1][col2]
            plain += matrix[row2][col1]
    return plain

# -------------------------------
# Chạy chương trình chính (input trực tiếp)
# -------------------------------
if __name__ == "__main__":
    key = input("Nhập từ khóa (key): ").strip()
    plaintext = input("Nhập plaintext: ").strip()

    cipher = playfair_encrypt(plaintext, key)
    print("Ciphertext:", cipher)

    decoded = playfair_decrypt(cipher, key)
    print("Decoded   :", decoded)
