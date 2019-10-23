#!/usr/bin/env bash
OUTPUT=$1
if [[ -z ${OUTPUT} ]]
then
    echo "Args: <output directory>"
    exit
fi

echo -n "UFSCID: "
read UFSCID
echo -n "Password: "
read -s PASSWD
echo

SEMESTER=20192

function validate() {
    local subject=$1
    local class=$2
    local semester=$3
    echo python -m attor validate $subject $class $SEMESTER ${OUTPUT} --ufscid ${UFSCID} --passwd ${APASSWD}
}

# 1ª Fase
validate INE5401 01208A

validate INE5402 01208A
validate INE5402 01208B
validate INE5402 01208C

validate INE5403 01208A
validate INE5403 01208B

# 2ª Fase
validate INE5404 02208A
validate INE5404 02208B

validate INE5405 02208A
validate INE5405 05222

validate INE5406 02208A
validate INE5406 02208B
validate INE5406 05235A

validate INE5407 02208A
validate INE5407 02208B
validate INE5407 07202A
validate INE5407 07202B
validate INE5407 09235A
validate INE5407 09235B

# 3ª Fase
validate INE5408 03208A

validate INE5409 03208

validate INE5410 03208A
validate INE5410 03208B

validate INE5411 03208A
validate INE5411 03208C
validate INE5411 06235

# 4ª Fase
validate INE5412 04208A
validate INE5413 04208
validate INE5414 04208
validate INE5416 04208

validate INE5417 04208A
validate INE5417 04208B

# 5ª Fase
validate INE5418 05208
validate INE5419 05208
validate INE5420 05208
validate INE5421 05208
validate INE5422 05208
validate INE5423 05208

# 6ª Fase
validate INE5424 06208
validate INE5425 06208
validate INE5426 06208
validate INE5427 06208
validate INE5430 06208

# 7ª Fase
validate INE5428 07208
validate INE5429 07208
validate INE5431 07208
validate INE5432 07208
validate INE5433 07208

# Optativas
validate INE5443 05208
validate INE5444 05208
validate INE5445 06208
validate INE5449 05208
validate INE5450 08208
validate INE5452 08208
validate INE5453 06208

validate INE5454 05238
validate INE5454 06208

validate INE5461 07208
validate INE5462 07208
validate INE5463 08208
