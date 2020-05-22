FROM python:3.7.3

# Create work dir
WORKDIR /app/

# Install Python packages
COPY /requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY . /app/

# Add database polling tool
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait ./wait
RUN chmod +x ./wait

# Prepare container interface
RUN chmod +x ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]