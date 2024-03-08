--
-- Cơ sở dữ liệu: `nln`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `user_favorite`
--

CREATE TABLE `user_favorite` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `thesis_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `user_favorite`
--

INSERT INTO `user_favorite` (`id`, `user_id`, `thesis_id`) VALUES
(10, 2, 6),
(13, 2, 2),
(24, 2, 5);

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `user_favorite`
--
ALTER TABLE `user_favorite`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `thesis_id` (`thesis_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `user_favorite`
--
ALTER TABLE `user_favorite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `user_favorite`
--
ALTER TABLE `user_favorite`
  ADD CONSTRAINT `user_favorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `user_favorite_ibfk_2` FOREIGN KEY (`thesis_id`) REFERENCES `data` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
