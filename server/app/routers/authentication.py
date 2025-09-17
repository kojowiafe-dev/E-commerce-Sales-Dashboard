
# @router.post("/forgot-password")
# async def forgot_password(
#     request: schemas.ForgotPasswordRequest,
#     session: database.SessionDep
# ):
#     email = request.email

#     # check if the user exists
#     user = session.exec(
#         select(model.User).where(model.User.email == email)
#     ).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Email not found"
#         )
    
#     # Generate OTP and expiry
#     try:
#         code = otp.generate_otp()
#         expires_at = otp.get_expiry()
    
#     except Exception as e:
#         logging.error(f"Error generating OTP: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error generating OTP: {str(e)}"
#         )
        
#     try:
#         reset_entry = model.PasswordResetCode(
#             email = email,
#             code = code,
#             expires_at = expires_at
#         )
#         session.add(reset_entry)
#         session.commit()

#     except Exception as e:
#         session.rollback()
#         logging.error(f"Database error: {str(e)}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Database error: {str(e)}"
#         )
    
#     # Send OTP via email
#     try:
#         await mail.send_verification_email(
#             email,
#             "Your password reset code",
#             f"Your OTP is: {code}"
#         )
#     except Exception as e:
#         logging.error(f"Failed to send email: {e}")
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to send email: {str(e)}"
#         )

#     return {"msg": "OTP sent to email"}


# @router.post("/verify-code")
# async def verify_code(data: schemas.VerifyResetCodeRequest, session: database.SessionDep):
#     entry = (
#         session.exec(select(model.PasswordResetCode).where(model.PasswordResetCode.email == data.email, 
#                 model.PasswordResetCode.code == data.code)
#         .order_by(model.PasswordResetCode.created_at.desc())
#         )
#         .first()
#     )

#     if not entry or entry.expires_at < datetime.utcnow():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired code")
    
#     return {"msg": "Code verified"}

    
# @router.post("/reset-password")
# async def reset_password(
#     data: schemas.ResetPasswordRequest,
#     session: Annotated[Session, Depends(database.get_session)]
# ):
#     statement = select(model.PasswordResetCode).where(
#         (model.PasswordResetCode.email == data.email) &
#         (model.PasswordResetCode.code == data.code) &
#         (model.PasswordResetCode.verified == True)
#     )
#     statement = statement.order_by(model.PasswordResetCode.created_at.desc())
#     entry = session.exec(statement).first()
#     if not entry or entry.expires_at < datetime.utcnow():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired code")

#     statement = select(model.User).where(model.User.email == data.email)
#     user = session.exec(statement).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

#     hashed_pw = hashing.pass_context.hash(data.new_password)
#     user.password = hashed_pw
#     session.commit()
#     return {"msg": "Password reset successful"}


# @router.post("/verify-reset-code")
# async def verify_reset_code(
#     data: schemas.VerifyResetCodeRequest,
#     session: Annotated[Session, Depends(database.get_session)]
# ):
#     if not data.code.isdigit() or len(data.code) != 6:
#         raise HTTPException(status_code=400, detail="Code must be a 6-digit number")

#     statement = select(model.PasswordResetCode).where(
#         (model.PasswordResetCode.email == data.email) &
#         (model.PasswordResetCode.code == data.code)
#     )
#     statement = statement.order_by(model.PasswordResetCode.created_at.desc())
#     entry = session.exec(statement).first()

#     if not entry or entry.expires_at < datetime.utcnow():
#         raise HTTPException(status_code=400, detail="Invalid or expired code")

#     entry.verified = True
#     session.commit()

#     return {"msg": "Code verified successfully"}
