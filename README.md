
# MySide API
Essa é uma API desenvolvida como teste técnico para a MySide. Feita utilizando FastAPI como framework backend e se comunicando com um banco de dados PostgreSQL. Toda a aplicação está contida em um contâiner Docker.

## Requisitos
* Docker

## Como rodar
Primeiro, precisamos clonar o repositório do Github.
```git clone https://github.com/undead-myauti/my-side-api.git```

> Caso você queira, é possível clonar via ssh também!

> **Antes de passarmos para o próximo passo, certifique-se de que você possui o Docker instalado em sua máquina. Caso não tenha, siga a [documentação](https://docs.docker.com/engine/install/) e faça a instalação!**

Agora, com o repo clonado, vamos acessá-lo e subir nosso container com a aplicação
e nosso banco.

```
cd my-side-api
docker compose up -d
```

Com os comandos acima, você entrará na pasta do repositório e subirá o container contendo o PostgreSQL e a nossa API 🙂

Para conferir se está tudo ok, use ```docker ps```, caso o status dos dois serviços estiver definido como **UP** é porque estamos prontos para começar a utilizar a API!

# Lista de endpoints
Abaixo está descrito os endpoints existentes no projeto e o que deve ser passado como parâmetro.

Para testá-los, você pode usar a própria documentação gerada pelo Swagger acessando:

```http://localhost:8000/docs```

Lá você encontrará mais detalhes sobre cada rota.

> **Atenção, com o endpoint DELETE /user/{email}. Para utilizá-lo, é necessário gerar um token antes.**

### POST
#### Cadastro de uma sala

```http
  POST /rooms
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `name`| `string` | **Required**|
| `capacity`| `int` | **Required**|
| `location`| `string` | **Required**|

#### Reservar uma sala

```http
  POST /reservations
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `room_id`      | `int` | **Required**|
| `user_name`      | `string` | **Required**|
| `start_time`      | `string` | **Required**|
| `end_time`      | `string` | **Required**|
| `owner_email`      | `string` | **Required**|

#### Criar um usuário
```http
  POST /register
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `int` | **Required**|
| `email`      | `string` | **Required**|
| `password`      | `string` | **Required**|

#### Criar um token
```http
  POST /token
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `int` | **Required**|
| `email`      | `string` | **Required**|
| `password`      | `string` | **Required**|


### GET

#### Exibir todas as salas

```http
  GET /rooms
```


#### Exibir disponibilidade de uma sala em um período de tempo

```http
  GET /rooms/{id}/availability
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required as URL param**|
| `start_time`      | `string` | **Required as URL param** |
| `end_time`      | `string` | **Required as URL param**|

#### Exibir todas as reservas de uma sala ou as reservas para uma data específica

```http
  GET /rooms/{id}/reservations
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required as URL param**|
| `date`      | `string` | **Optional as URL param** |

#### Exibir uma reserva

```http
  GET /reservation/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | **Required as URL param**|


#### Exibir usuário

```http
  GET /user/{email}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `email`      | `string` | **Required as URL param**|


### DELETE

#### Deletar uma reserva

```http
  DELETE /user/{email}
```
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required as URL param**|
| `token`      | `string` | **Required as URL param**|

