export DITTO_PATH="PATH_TO_THE_DITTO_ROOT_FOLDER"

ditto-this()
{
    python "$DITTO_PATH/src/ditto.py" "$@"
}

ditto-filter()
{
    python "$DITTO_PATH/src/ditto.py" --keep-datatype "$@"
}