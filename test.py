def my_sort(books):
    for i in range(len(books)):
        index = i
        min_book = books[i]
        for j in range(i, len(books)):
            if books[j] <= min_book:
                min_book = books[j]
                index = j
        books[i], books[index] = books[index], books[i]
    return books


books = [1000, 5, -9, 400, 20]
books = my_sort(books)
print(*books)
