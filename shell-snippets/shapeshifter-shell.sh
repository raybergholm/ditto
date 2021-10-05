export SHAPESHIFTER_PATH="PATH_TO_THIS_ROOT_FOLDER"

shapeshift-me()
{
    python "$SHAPESHIFTER_PATH/src/shapeshifter_cli.py" "$@"
}

shapeshift-filter()
{
    python "$SHAPESHIFTER_PATH/src/shapeshifter_cli.py" --keep-datatype "$@"
}