/*
  Warnings:

  - The primary key for the `AuditLog` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `api_endpoint` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `created_at` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `log_id` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `request_payload` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `response_payload` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `status_code` on the `AuditLog` table. All the data in the column will be lost.
  - The primary key for the `Conversation` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `conversation_id` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `conversation_type` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `end_time` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `start_time` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Conversation` table. All the data in the column will be lost.
  - The primary key for the `Media` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `created_at` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `media_id` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `media_size` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `media_type` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `media_url` on the `Media` table. All the data in the column will be lost.
  - The primary key for the `Message` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `created_at` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `group_id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `media_id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `message_id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `message_type` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `template_id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `tenant_id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `updated_at` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `Message` table. All the data in the column will be lost.
  - You are about to alter the column `direction` on the `Message` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Enum(EnumId(0))`.
  - You are about to alter the column `status` on the `Message` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Enum(EnumId(2))`.
  - The primary key for the `Setting` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `setting_id` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `setting_name` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `setting_value` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `updated_at` on the `Setting` table. All the data in the column will be lost.
  - The primary key for the `Template` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `created_at` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `language_code` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `template_body` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `template_id` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `template_name` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `tenant_id` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `updated_at` on the `Template` table. All the data in the column will be lost.
  - You are about to alter the column `status` on the `Template` table. The data in that column could be lost. The data in that column will be cast from `VarChar(191)` to `Enum(EnumId(4))`.
  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `created_at` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `opt_in_status` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `phone_number` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `tenant_id` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `updated_at` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `user_id` on the `User` table. All the data in the column will be lost.
  - The primary key for the `Webhook` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `event_type` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the column `received_at` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the column `webhook_id` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the `Group` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `GroupMember` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Tenant` table. If the table is not empty, all the data it contains will be lost.
  - A unique constraint covering the columns `[settingName]` on the table `Setting` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[phoneNumber]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `apiEndpoint` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `requestPayload` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `statusCode` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `conversationType` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `userId` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Made the column `pricing` on table `Conversation` required. This step will fail if there are existing NULL values in that column.
  - Added the required column `id` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `mediaType` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `mediaUrl` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `messageType` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `userId` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `settingName` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `settingValue` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `languageCode` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `templateBody` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `templateName` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `phoneNumber` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updatedAt` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `eventType` to the `Webhook` table without a default value. This is not possible if the table is not empty.
  - Added the required column `id` to the `Webhook` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `Conversation` DROP FOREIGN KEY `Conversation_user_id_fkey`;

-- DropForeignKey
ALTER TABLE `Group` DROP FOREIGN KEY `Group_tenant_id_fkey`;

-- DropForeignKey
ALTER TABLE `GroupMember` DROP FOREIGN KEY `GroupMember_group_id_fkey`;

-- DropForeignKey
ALTER TABLE `GroupMember` DROP FOREIGN KEY `GroupMember_user_id_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_group_id_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_media_id_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_template_id_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_tenant_id_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_user_id_fkey`;

-- DropForeignKey
ALTER TABLE `Template` DROP FOREIGN KEY `Template_tenant_id_fkey`;

-- DropForeignKey
ALTER TABLE `User` DROP FOREIGN KEY `User_tenant_id_fkey`;

-- DropIndex
DROP INDEX `Conversation_user_id_fkey` ON `Conversation`;

-- DropIndex
DROP INDEX `Message_group_id_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_media_id_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_template_id_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_tenant_id_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_user_id_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Setting_setting_name_key` ON `Setting`;

-- DropIndex
DROP INDEX `Template_tenant_id_fkey` ON `Template`;

-- DropIndex
DROP INDEX `User_phone_number_key` ON `User`;

-- DropIndex
DROP INDEX `User_tenant_id_fkey` ON `User`;

-- AlterTable
ALTER TABLE `AuditLog` DROP PRIMARY KEY,
    DROP COLUMN `api_endpoint`,
    DROP COLUMN `created_at`,
    DROP COLUMN `log_id`,
    DROP COLUMN `request_payload`,
    DROP COLUMN `response_payload`,
    DROP COLUMN `status_code`,
    ADD COLUMN `apiEndpoint` VARCHAR(191) NOT NULL,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `requestPayload` JSON NOT NULL,
    ADD COLUMN `responsePayload` JSON NULL,
    ADD COLUMN `statusCode` INTEGER NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Conversation` DROP PRIMARY KEY,
    DROP COLUMN `conversation_id`,
    DROP COLUMN `conversation_type`,
    DROP COLUMN `end_time`,
    DROP COLUMN `start_time`,
    DROP COLUMN `user_id`,
    ADD COLUMN `conversationType` ENUM('business_initiated', 'user_initiated') NOT NULL,
    ADD COLUMN `endTime` DATETIME(3) NULL,
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `startTime` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `userId` INTEGER NOT NULL,
    MODIFY `pricing` DECIMAL(10, 2) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Media` DROP PRIMARY KEY,
    DROP COLUMN `created_at`,
    DROP COLUMN `media_id`,
    DROP COLUMN `media_size`,
    DROP COLUMN `media_type`,
    DROP COLUMN `media_url`,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `mediaSize` INTEGER NULL,
    ADD COLUMN `mediaType` ENUM('image', 'video', 'document', 'audio') NOT NULL,
    ADD COLUMN `mediaUrl` VARCHAR(191) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Message` DROP PRIMARY KEY,
    DROP COLUMN `created_at`,
    DROP COLUMN `group_id`,
    DROP COLUMN `media_id`,
    DROP COLUMN `message_id`,
    DROP COLUMN `message_type`,
    DROP COLUMN `template_id`,
    DROP COLUMN `tenant_id`,
    DROP COLUMN `updated_at`,
    DROP COLUMN `user_id`,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `mediaId` INTEGER NULL,
    ADD COLUMN `messageType` ENUM('text', 'media', 'template', 'interactive') NOT NULL,
    ADD COLUMN `templateId` INTEGER NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    ADD COLUMN `userId` INTEGER NOT NULL,
    MODIFY `direction` ENUM('incoming', 'outgoing') NOT NULL,
    MODIFY `status` ENUM('sent', 'delivered', 'read', 'failed') NOT NULL DEFAULT 'sent',
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Setting` DROP PRIMARY KEY,
    DROP COLUMN `setting_id`,
    DROP COLUMN `setting_name`,
    DROP COLUMN `setting_value`,
    DROP COLUMN `updated_at`,
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `settingName` VARCHAR(191) NOT NULL,
    ADD COLUMN `settingValue` VARCHAR(191) NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Template` DROP PRIMARY KEY,
    DROP COLUMN `created_at`,
    DROP COLUMN `language_code`,
    DROP COLUMN `template_body`,
    DROP COLUMN `template_id`,
    DROP COLUMN `template_name`,
    DROP COLUMN `tenant_id`,
    DROP COLUMN `updated_at`,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `languageCode` VARCHAR(191) NOT NULL,
    ADD COLUMN `templateBody` VARCHAR(191) NOT NULL,
    ADD COLUMN `templateName` VARCHAR(191) NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    MODIFY `status` ENUM('approved', 'pending', 'rejected') NOT NULL DEFAULT 'pending',
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `User` DROP PRIMARY KEY,
    DROP COLUMN `created_at`,
    DROP COLUMN `opt_in_status`,
    DROP COLUMN `phone_number`,
    DROP COLUMN `tenant_id`,
    DROP COLUMN `updated_at`,
    DROP COLUMN `user_id`,
    ADD COLUMN `createdAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `optInStatus` BOOLEAN NOT NULL DEFAULT true,
    ADD COLUMN `phoneNumber` VARCHAR(191) NOT NULL,
    ADD COLUMN `updatedAt` DATETIME(3) NOT NULL,
    ADD PRIMARY KEY (`id`);

-- AlterTable
ALTER TABLE `Webhook` DROP PRIMARY KEY,
    DROP COLUMN `event_type`,
    DROP COLUMN `received_at`,
    DROP COLUMN `webhook_id`,
    ADD COLUMN `eventType` VARCHAR(191) NOT NULL,
    ADD COLUMN `id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `receivedAt` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD PRIMARY KEY (`id`);

-- DropTable
DROP TABLE `Group`;

-- DropTable
DROP TABLE `GroupMember`;

-- DropTable
DROP TABLE `Tenant`;

-- CreateIndex
CREATE UNIQUE INDEX `Setting_settingName_key` ON `Setting`(`settingName`);

-- CreateIndex
CREATE UNIQUE INDEX `User_phoneNumber_key` ON `User`(`phoneNumber`);

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_mediaId_fkey` FOREIGN KEY (`mediaId`) REFERENCES `Media`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_templateId_fkey` FOREIGN KEY (`templateId`) REFERENCES `Template`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Conversation` ADD CONSTRAINT `Conversation_userId_fkey` FOREIGN KEY (`userId`) REFERENCES `User`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
