package util

import (
	"fmt"
	"github.com/go-faster/errors"
	"io"
	"os"
	"path/filepath"
)

func MoveFiles(srcDir, dstDir string) error {
	// 确保目标目录存在
	if err := os.MkdirAll(dstDir, os.ModePerm); err != nil {
		return errors.Wrap(err, "创建目标目录失败")
	}

	// 读取源目录的文件
	entries, err := os.ReadDir(srcDir)
	if err != nil {
		return errors.Wrap(err, "读取源目录失败")
	}

	for _, entry := range entries {
		if entry.IsDir() {
			continue // 跳过子目录, 只处理文件
		}

		srcPath := filepath.Join(srcDir, entry.Name())
		dstPath := filepath.Join(dstDir, entry.Name())

		// 移动文件
		if err := MoveFile(srcPath, dstPath); err != nil {
			return errors.Wrapf(err, "移动文件 %s 失败\n", srcPath)
		} else {
			fmt.Printf("成功移动文件: %s -> %s\n", srcPath, dstPath)
		}
	}

	return nil
}

// moveFile 移动文件（适用于跨设备文件系统）
func MoveFile(src, dst string) error {
	// 先尝试重命名（适用于同一文件系统）
	if err := os.Rename(src, dst); err == nil {
		return nil
	}

	// 如果 Rename 失败，可能是跨设备移动，尝试复制后删除
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()

	dstFile, err := os.OpenFile(dst, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0666)
	if err != nil {
		return err
	}
	defer dstFile.Close()

	// 复制文件内容
	buf := make([]byte, 1024*1024*5) // 32KB 缓冲区
	if _, err := io.CopyBuffer(dstFile, srcFile, buf); err != nil {
		return err
	}

	// 确保数据写入磁盘
	if err := dstFile.Sync(); err != nil {
		return err
	}

	// 删除源文件
	return os.Remove(src)
}
