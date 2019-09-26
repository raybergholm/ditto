export DITTO_PATH="PATH TO THE DITTO FOLDER"

ditto-me()
{
    python "$DITTO_PATH/src/ditto.py" "$@"
}