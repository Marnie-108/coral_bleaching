import umpyutl as umpy

def main() -> None:
    """Entry point. Orchestrates workflow.

    Parameters:
        None

    Returns:
        None
    """

    data = umpy.read.from_csv("./coral_bleaching.csv")

    reefs = sorted(data[1:], key=lambda x: int(x[0]))
    umpy.write.to_csv("./coral_bleaching-sorted.csv", reefs, data[0])


if __name__ == "__main__":
    main()