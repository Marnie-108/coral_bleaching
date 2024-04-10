import umpyutl as umpy

def main() -> None:
    """Entry point. Orchestrates workflow.

    Parameters:
        None

    Returns:
        None
    """

    data = umpy.read.from_csv("./coral_bleaching.csv")

    # Check values
    # count = 0
    # for i in range(1, len(data)):
    #     data[i][0] = umpy.convert.str_to_int(data[i][0])
    #     if not isinstance(data[i][0], int):
    #         count += 1
    # print(f"\n count = {count}")

    reefs = sorted(data[1:], key=lambda x: int(x[0]))
    umpy.write.to_csv("./coral_bleaching-sorted.csv", reefs, data[0])


if __name__ == "__main__":
    main()