ARG GO_VERSION=1.25 
FROM golang:${GO_VERSION}-alpine AS builder

ENV CGO_ENABLED=0 GOOS=lunix 
WORKDIR /src 

COPY go.mod go.sum ./
RUN go mod download

COPY . .
ARG MAIN=./cmd/server 
RUN go build -trimpath -ldflags="-s -w" -o /out/app ${MAIN}

# Runtime 
FROM gcr.io/distroless/static:nonroot

WORKDIR /app
COPY --from=builder /out/app /app/app 

USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app/app"]
