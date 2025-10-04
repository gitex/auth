from src.claims import Claims
from src.codecs.jose import JoseJwtCodec


def test_codec_should_encode_and_decode_back_claims(
    jwt_codec: JoseJwtCodec, access_claims: Claims
) -> None:
    token = jwt_codec.encode(access_claims)
    result_claims = jwt_codec.decode(token, audience=access_claims.aud)

    assert result_claims == access_claims
