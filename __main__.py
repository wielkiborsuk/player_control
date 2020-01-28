from control.control import DelegatingController


def main():
    controller = DelegatingController()
    # controller.focus('spotify')
    print(controller.status())
    controller.next()


if __name__ == "__main__":
    main()
