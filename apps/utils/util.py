from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import random



def random_device_id():
    str_16 = "0123456789abcdef"
    # num_16 = "".join([hex(random.randint(0, 15))[-1:] for _ in range(19)])
    # num_16 = "".join([random.choice(a) for i in range(19)])
    num_16 = "".join(random.choices(str_16, k=19))

    return num_16



class Aescrypt:
    def __init__(self):
        self.key = '0CoJUm6Qyw8W8jud'
        self.iv = '1234567812345678'
        self.mode = AES.MODE_CBC
        self.BLOCK_SIZE = AES.block_size
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE) * chr(
            self.BLOCK_SIZE - len(s.encode()) % self.BLOCK_SIZE)
        # 去除补位
        self.un_pad = lambda s: s[:-ord(s[len(s) - 1:])]
        # 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)

    def encrypt_aes(self, a_text):
        """
        加密 ：先补位，再AES加密，后base64编码
        :param text: 需加密的明文
        :return:
        """
        # text = pad(text) 包pycrypto的写法，加密函数可以接受str也可以接受bytess
        text = self.pad(a_text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode(), mode=self.mode, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt_aes(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=self.mode, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.un_pad(decrypted_text).decode('utf-8')


if __name__ == '__main__':
    aescrypt = Aescrypt()  # CBC模式
    # text = "456123qwe1胡成3213强大的"
    # en_text = aescrypt.encrypt_aes(text)
    # print("密文:", en_text)
    text = aescrypt.decrypt_aes("HF1qG5O/WWsIuD0TMVQg7own1hq24Jf4pdsD1VQOeeBhmb01gWGOe3Wa4iRfhAs8XrTtTlFNkTvQv7/T4/sGSJU6LtqX3LU9RwIRe3rn1CV6T/jesIlwF2cGtzqpi9A3oy6igRJtiHDM2OJMQvCcxHJJp5Bq9hcs3zqQOkvypaWepbyrxRUnOrSt2kDsCepR4a8dAq9NgpqMtKqSmQOMEQoipQrYGZBunPprgMG7WUXfe/M3A7R0wOJOCSuQzpfC9YNNbeUDEyFsn6pK90mJ1w+G7EOdWb2B9DfJ3hf1AQjkLjumlwmcKcxD1ypm63rt0yDl9wrbWl6rbXrTYbJjhNOizxtHtDcoHeLVshCU7sFe3mbmoHd+vnI9H4fcfejnTpwI8hjzWLX772UVExFxidQLDJMjDC8BanhGyru6Nr6Gy4V6UeJGSSJUDNkokkR5xR9UFEuV8ldcNi0vq7VwjDUTOwC3Ye4qn9rPKcjkZW6IXopLoviyusGLNlmOKzJD")
    print(text)
