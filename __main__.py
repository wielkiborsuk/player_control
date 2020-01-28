from control.control import DelegatingController


def main():
    controller = DelegatingController()
    controller.focus('cmus')
    # print(controller.status())
    # controller.next()
    controller.toggle()


if __name__ == "__main__":
    main()
