import datetime
import ipaddress
import os

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
)
from cryptography.x509 import SubjectAlternativeName
from cryptography.x509.oid import NameOID


def generate_certificate(ip_sans=None):
    """
    生成ssl自签名证书
    :return:
    """
    # 生成私钥
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())

    # 准备证书信息
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COUNTRY_NAME, "CN"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Beijing"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Beijing"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "K8s Operator Framework"),
            x509.NameAttribute(NameOID.COMMON_NAME, "k8s.operator.com"),
        ]
    )

    # 生成证书
    cert_builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=36500))
    )

    # 添加 DNSName 和 IPAddress
    alt_names = [x509.DNSName("localhost")]
    if ip_sans:
        alt_names.extend(x509.IPAddress(ipaddress.ip_address(ip)) for ip in ip_sans)

        cert_builder = cert_builder.add_extension(
            SubjectAlternativeName(alt_names),
            critical=False,
        )

    cert = cert_builder.sign(private_key, hashes.SHA256(), default_backend())

    work_dir = os.getcwd()
    cert_dir = os.path.join(work_dir, ".cert")
    if not os.path.exists(cert_dir):
        os.makedirs(cert_dir)

    private_key_file_path = os.path.join(cert_dir, "private.key")
    cert_file_path = os.path.join(cert_dir, "cert.crt")

    # 保存私钥到文件
    with open(private_key_file_path, "wb") as f:
        f.write(private_key.private_bytes(Encoding.PEM, PrivateFormat.TraditionalOpenSSL, NoEncryption()))

    # 保存证书到文件
    with open(cert_file_path, "wb") as f:
        f.write(cert.public_bytes(Encoding.PEM))

    return private_key_file_path, cert_file_path
