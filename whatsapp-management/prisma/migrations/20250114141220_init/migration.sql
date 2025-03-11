/*
  Warnings:

  - The primary key for the `AuditLog` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `apiEndpoint` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `createdAt` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `requestPayload` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `responsePayload` on the `AuditLog` table. All the data in the column will be lost.
  - You are about to drop the column `statusCode` on the `AuditLog` table. All the data in the column will be lost.
  - The primary key for the `Conversation` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `conversationType` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `endTime` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `startTime` on the `Conversation` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `Conversation` table. All the data in the column will be lost.
  - You are about to alter the column `pricing` on the `Conversation` table. The data in that column could be lost. The data in that column will be cast from `Decimal(10,2)` to `Double`.
  - The primary key for the `Media` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `createdAt` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `mediaSize` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `mediaType` on the `Media` table. All the data in the column will be lost.
  - You are about to drop the column `mediaUrl` on the `Media` table. All the data in the column will be lost.
  - The primary key for the `Message` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `createdAt` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `mediaId` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `messageType` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `templateId` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `updatedAt` on the `Message` table. All the data in the column will be lost.
  - You are about to drop the column `userId` on the `Message` table. All the data in the column will be lost.
  - You are about to alter the column `direction` on the `Message` table. The data in that column could be lost. The data in that column will be cast from `Enum(EnumId(2))` to `VarChar(191)`.
  - You are about to alter the column `status` on the `Message` table. The data in that column could be lost. The data in that column will be cast from `Enum(EnumId(5))` to `VarChar(191)`.
  - The primary key for the `Setting` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `settingName` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `settingValue` on the `Setting` table. All the data in the column will be lost.
  - You are about to drop the column `updatedAt` on the `Setting` table. All the data in the column will be lost.
  - The primary key for the `Template` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `createdAt` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `languageCode` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `templateBody` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `templateName` on the `Template` table. All the data in the column will be lost.
  - You are about to drop the column `updatedAt` on the `Template` table. All the data in the column will be lost.
  - You are about to alter the column `status` on the `Template` table. The data in that column could be lost. The data in that column will be cast from `Enum(EnumId(4))` to `VarChar(191)`.
  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `createdAt` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `optInStatus` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `phoneNumber` on the `User` table. All the data in the column will be lost.
  - You are about to drop the column `updatedAt` on the `User` table. All the data in the column will be lost.
  - The primary key for the `Webhook` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `eventType` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the column `id` on the `Webhook` table. All the data in the column will be lost.
  - You are about to drop the column `receivedAt` on the `Webhook` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[setting_name]` on the table `Setting` will be added. If there are existing duplicate values, this will fail.
  - A unique constraint covering the columns `[phone_number]` on the table `User` will be added. If there are existing duplicate values, this will fail.
  - Added the required column `api_endpoint` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `log_id` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `request_payload` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `status_code` to the `AuditLog` table without a default value. This is not possible if the table is not empty.
  - Added the required column `conversation_id` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `conversation_type` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_id` to the `Conversation` table without a default value. This is not possible if the table is not empty.
  - Added the required column `media_id` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `media_type` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `media_url` to the `Media` table without a default value. This is not possible if the table is not empty.
  - Added the required column `message_id` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `message_type` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `tenant_id` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_id` to the `Message` table without a default value. This is not possible if the table is not empty.
  - Added the required column `setting_id` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `setting_name` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `setting_value` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `Setting` table without a default value. This is not possible if the table is not empty.
  - Added the required column `language_code` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `template_body` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `template_id` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `template_name` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `tenant_id` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `Template` table without a default value. This is not possible if the table is not empty.
  - Added the required column `phone_number` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `tenant_id` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `updated_at` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `user_id` to the `User` table without a default value. This is not possible if the table is not empty.
  - Added the required column `event_type` to the `Webhook` table without a default value. This is not possible if the table is not empty.
  - Added the required column `webhook_id` to the `Webhook` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `Conversation` DROP FOREIGN KEY `Conversation_userId_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_mediaId_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_templateId_fkey`;

-- DropForeignKey
ALTER TABLE `Message` DROP FOREIGN KEY `Message_userId_fkey`;

-- DropIndex
DROP INDEX `Conversation_userId_fkey` ON `Conversation`;

-- DropIndex
DROP INDEX `Message_mediaId_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_templateId_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Message_userId_fkey` ON `Message`;

-- DropIndex
DROP INDEX `Setting_settingName_key` ON `Setting`;

-- DropIndex
DROP INDEX `User_phoneNumber_key` ON `User`;

-- AlterTable
ALTER TABLE `AuditLog` DROP PRIMARY KEY,
    DROP COLUMN `apiEndpoint`,
    DROP COLUMN `createdAt`,
    DROP COLUMN `id`,
    DROP COLUMN `requestPayload`,
    DROP COLUMN `responsePayload`,
    DROP COLUMN `statusCode`,
    ADD COLUMN `api_endpoint` VARCHAR(191) NOT NULL,
    ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `log_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `request_payload` JSON NOT NULL,
    ADD COLUMN `response_payload` JSON NULL,
    ADD COLUMN `status_code` INTEGER NOT NULL,
    ADD PRIMARY KEY (`log_id`);

-- AlterTable
ALTER TABLE `Conversation` DROP PRIMARY KEY,
    DROP COLUMN `conversationType`,
    DROP COLUMN `endTime`,
    DROP COLUMN `id`,
    DROP COLUMN `startTime`,
    DROP COLUMN `userId`,
    ADD COLUMN `conversation_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `conversation_type` VARCHAR(191) NOT NULL,
    ADD COLUMN `end_time` DATETIME(3) NULL,
    ADD COLUMN `start_time` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `user_id` INTEGER NOT NULL,
    MODIFY `pricing` DOUBLE NULL,
    ADD PRIMARY KEY (`conversation_id`);

-- AlterTable
ALTER TABLE `Media` DROP PRIMARY KEY,
    DROP COLUMN `createdAt`,
    DROP COLUMN `id`,
    DROP COLUMN `mediaSize`,
    DROP COLUMN `mediaType`,
    DROP COLUMN `mediaUrl`,
    ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `media_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `media_size` INTEGER NULL,
    ADD COLUMN `media_type` VARCHAR(191) NOT NULL,
    ADD COLUMN `media_url` VARCHAR(191) NOT NULL,
    ADD PRIMARY KEY (`media_id`);

-- AlterTable
ALTER TABLE `Message` DROP PRIMARY KEY,
    DROP COLUMN `createdAt`,
    DROP COLUMN `id`,
    DROP COLUMN `mediaId`,
    DROP COLUMN `messageType`,
    DROP COLUMN `templateId`,
    DROP COLUMN `updatedAt`,
    DROP COLUMN `userId`,
    ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `group_id` INTEGER NULL,
    ADD COLUMN `media_id` INTEGER NULL,
    ADD COLUMN `message_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `message_type` VARCHAR(191) NOT NULL,
    ADD COLUMN `template_id` INTEGER NULL,
    ADD COLUMN `tenant_id` INTEGER NOT NULL,
    ADD COLUMN `updated_at` DATETIME(3) NOT NULL,
    ADD COLUMN `user_id` INTEGER NOT NULL,
    MODIFY `direction` VARCHAR(191) NOT NULL,
    MODIFY `status` VARCHAR(191) NOT NULL DEFAULT 'sent',
    ADD PRIMARY KEY (`message_id`);

-- AlterTable
ALTER TABLE `Setting` DROP PRIMARY KEY,
    DROP COLUMN `id`,
    DROP COLUMN `settingName`,
    DROP COLUMN `settingValue`,
    DROP COLUMN `updatedAt`,
    ADD COLUMN `setting_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `setting_name` VARCHAR(191) NOT NULL,
    ADD COLUMN `setting_value` VARCHAR(191) NOT NULL,
    ADD COLUMN `updated_at` DATETIME(3) NOT NULL,
    ADD PRIMARY KEY (`setting_id`);

-- AlterTable
ALTER TABLE `Template` DROP PRIMARY KEY,
    DROP COLUMN `createdAt`,
    DROP COLUMN `id`,
    DROP COLUMN `languageCode`,
    DROP COLUMN `templateBody`,
    DROP COLUMN `templateName`,
    DROP COLUMN `updatedAt`,
    ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `language_code` VARCHAR(191) NOT NULL,
    ADD COLUMN `template_body` VARCHAR(191) NOT NULL,
    ADD COLUMN `template_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD COLUMN `template_name` VARCHAR(191) NOT NULL,
    ADD COLUMN `tenant_id` INTEGER NOT NULL,
    ADD COLUMN `updated_at` DATETIME(3) NOT NULL,
    MODIFY `status` VARCHAR(191) NOT NULL DEFAULT 'pending',
    ADD PRIMARY KEY (`template_id`);

-- AlterTable
ALTER TABLE `User` DROP PRIMARY KEY,
    DROP COLUMN `createdAt`,
    DROP COLUMN `id`,
    DROP COLUMN `optInStatus`,
    DROP COLUMN `phoneNumber`,
    DROP COLUMN `updatedAt`,
    ADD COLUMN `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `opt_in_status` BOOLEAN NOT NULL DEFAULT true,
    ADD COLUMN `phone_number` VARCHAR(191) NOT NULL,
    ADD COLUMN `tenant_id` INTEGER NOT NULL,
    ADD COLUMN `updated_at` DATETIME(3) NOT NULL,
    ADD COLUMN `user_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD PRIMARY KEY (`user_id`);

-- AlterTable
ALTER TABLE `Webhook` DROP PRIMARY KEY,
    DROP COLUMN `eventType`,
    DROP COLUMN `id`,
    DROP COLUMN `receivedAt`,
    ADD COLUMN `event_type` VARCHAR(191) NOT NULL,
    ADD COLUMN `received_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    ADD COLUMN `webhook_id` INTEGER NOT NULL AUTO_INCREMENT,
    ADD PRIMARY KEY (`webhook_id`);

-- CreateTable
CREATE TABLE `Tenant` (
    `tenant_id` INTEGER NOT NULL AUTO_INCREMENT,
    `tenant_name` VARCHAR(191) NOT NULL,
    `tenant_api_key` VARCHAR(191) NOT NULL,
    `tenant_status` VARCHAR(191) NOT NULL DEFAULT 'active',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updated_at` DATETIME(3) NOT NULL,

    UNIQUE INDEX `Tenant_tenant_api_key_key`(`tenant_api_key`),
    PRIMARY KEY (`tenant_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `Group` (
    `group_id` INTEGER NOT NULL AUTO_INCREMENT,
    `group_name` VARCHAR(191) NOT NULL,
    `group_description` VARCHAR(191) NULL,
    `group_status` VARCHAR(191) NOT NULL DEFAULT 'active',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `updated_at` DATETIME(3) NOT NULL,
    `tenant_id` INTEGER NOT NULL,

    PRIMARY KEY (`group_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateTable
CREATE TABLE `GroupMember` (
    `group_member_id` INTEGER NOT NULL AUTO_INCREMENT,
    `role` VARCHAR(191) NOT NULL DEFAULT 'member',
    `joined_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
    `group_id` INTEGER NOT NULL,
    `user_id` INTEGER NOT NULL,

    PRIMARY KEY (`group_member_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- CreateIndex
CREATE UNIQUE INDEX `Setting_setting_name_key` ON `Setting`(`setting_name`);

-- CreateIndex
CREATE UNIQUE INDEX `User_phone_number_key` ON `User`(`phone_number`);

-- AddForeignKey
ALTER TABLE `User` ADD CONSTRAINT `User_tenant_id_fkey` FOREIGN KEY (`tenant_id`) REFERENCES `Tenant`(`tenant_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Group` ADD CONSTRAINT `Group_tenant_id_fkey` FOREIGN KEY (`tenant_id`) REFERENCES `Tenant`(`tenant_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `GroupMember` ADD CONSTRAINT `GroupMember_group_id_fkey` FOREIGN KEY (`group_id`) REFERENCES `Group`(`group_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `GroupMember` ADD CONSTRAINT `GroupMember_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_tenant_id_fkey` FOREIGN KEY (`tenant_id`) REFERENCES `Tenant`(`tenant_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_group_id_fkey` FOREIGN KEY (`group_id`) REFERENCES `Group`(`group_id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_media_id_fkey` FOREIGN KEY (`media_id`) REFERENCES `Media`(`media_id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Message` ADD CONSTRAINT `Message_template_id_fkey` FOREIGN KEY (`template_id`) REFERENCES `Template`(`template_id`) ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Template` ADD CONSTRAINT `Template_tenant_id_fkey` FOREIGN KEY (`tenant_id`) REFERENCES `Tenant`(`tenant_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE `Conversation` ADD CONSTRAINT `Conversation_user_id_fkey` FOREIGN KEY (`user_id`) REFERENCES `User`(`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE;
