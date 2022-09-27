

def test_exception_1():
    raise Exception("test xiao")


if __name__ == "__main__":
    try:
        raise Exception("test")
    except Exception:
        print("success")