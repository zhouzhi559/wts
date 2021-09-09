
class Page:
    def __init__(self, currentPage, pageSize, rec_list):
        """

        :param totalPage: 总页数
        :param recordCount: 总记录数
        :param currentPage: 当前页
        :param pageSize:每页的数量
        """

        self.currentPage = currentPage
        self.pageSize = pageSize
        self.recordCount = len(rec_list)
        self.rec_list = rec_list
        self.totalPage, remainder = divmod(self.recordCount, self.pageSize)
        if remainder:
            self.totalPage += 1
        self.set_datas()

    def set_datas(self):
        start_index = (self.currentPage - 1) * self.pageSize
        end_index = self.currentPage * self.pageSize
        self.datas = self.rec_list[start_index:end_index]
        del self.rec_list

    def get_str_json(self):
        # return str(self.__dict__).replace("'", "\"")

        data_all = self.__dict__

        data = data_all["datas"]
        return data


# if __name__ == '__main__':
#     rec_list = [123, 456, 768, 111, 132, 65465, 999, 7887, 898,87]
#     page = Page(1, 3, rec_list)
#     print(page.get_str_json())