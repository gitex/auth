# @final
# class RefreshToken(Base):
#     __tablename__ = "refresh_tokens"
#
#     jti: Mapped[str] = mapped_column(String(64), primary_key=True)
#     account_id: Mapped[UUID] = mapped_column(
#         ForeignKey("accounts.id"), ondelete="CASCADE"
#     )
