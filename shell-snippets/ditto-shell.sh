export DITTO_PATH="PATH TO THE DITTO FOLDER"

ditto-this()
{
    python "$DITTO_PATH/src/ditto.py" "$@"
}