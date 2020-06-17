FROM dev.registry.ii-ai.tech/rpa/verification-code:base-v1
MAINTAINER pikaqiu

ADD ./source ./

EXPOSE 2020

WORKDIR rpa_ocr/verification_service/

ENTRYPOINT ["python", "main_service.py"]
